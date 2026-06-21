import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

from src.config import DATA_DIR
from src.ingestion.pipeline import run_ingestion
from src.ingestion.extractor import count_pdfs
from src.search.retriever import search, collection_count
from src.search.qa import answer_stream
from src.analytics.aggregator import (
    get_categories, resume_count,
    skill_frequency, seniority_distribution, experience_values,
)
from src.access.policy import ROLES, get_policy, redact

st.set_page_config(page_title="Resume Analyzer", layout="wide")

# ── Sidebar: role selector ────────────────────────────────────────────────────
with st.sidebar:
    st.header("Access Control")
    role = st.selectbox("Acting as", ROLES, index=0, key="role")
    policy = get_policy(role)

    st.divider()
    st.caption(f"**Active role:** {role}")
    if policy["allowed_categories"]:
        st.caption(f"**Scope:** {', '.join(policy['allowed_categories'])}")
    else:
        st.caption("**Scope:** All categories")
    if policy["redact_pii"]:
        st.caption("**PII:** Redacted")

st.title("Resume Analyzer")

ingestion_tab, search_tab, analytics_tab = st.tabs(["Ingestion", "Search", "Analytics"])

# ── Ingestion tab ─────────────────────────────────────────────────────────────
with ingestion_tab:
    st.header("Ingest Resumes")
    data_dir = st.text_input("Data folder path", value=str(DATA_DIR))

    if st.button("Start Ingestion", type="primary"):
        folder = Path(data_dir)
        if not folder.exists():
            st.error(f"Folder not found: {data_dir}")
            st.stop()

        total = count_pdfs(data_dir)
        if total == 0:
            st.error(f"No PDF files found in {data_dir}")
            st.stop()

        st.write(f"Found **{total}** PDFs. Starting ingestion…")
        progress_bar = st.progress(0.0)
        status_text = st.empty()
        error_log = st.expander("Errors", expanded=False)

        for event in run_ingestion(data_dir):
            if event["status"] == "complete":
                progress_bar.progress(1.0)
                status_text.empty()
                st.success(
                    f"Done — {event['total']} resumes processed "
                    f"({event['skipped']} skipped, {event.get('updated', 0)} updated, "
                    f"{event.get('deleted', 0)} deleted, {event['errors']} errors)"
                )
                if event["categories"]:
                    st.subheader("Ingested by category")
                    rows = sorted(event["categories"].items(), key=lambda x: -x[1])
                    st.dataframe(
                        {"Category": [r[0] for r in rows], "Resumes": [r[1] for r in rows]},
                        use_container_width=True,
                    )
            else:
                pct = event["processed"] / total
                progress_bar.progress(pct)
                if event["status"] == "done":
                    status_text.text(
                        f"[{event['processed']}/{total}] ✓ {event['resume_id']} "
                        f"({event['category']}) — {event['chunk_count']} chunks"
                    )
                elif event["status"] == "updated":
                    status_text.text(
                        f"[{event['processed']}/{total}] ↻ {event['resume_id']} "
                        f"({event['category']}) — {event['chunk_count']} chunks (updated)"
                    )
                elif event["status"] == "skipped":
                    status_text.text(f"[{event['processed']}/{total}] ⏭ {event['resume_id']} (unchanged)")
                elif event["status"] == "deleted":
                    status_text.text(f"[{event['processed']}/{total}] ✕ {event['resume_id']} (deleted from index)")
                elif event["status"] == "error":
                    status_text.text(f"[{event['processed']}/{total}] ✗ {event['resume_id']}")
                    error_log.write(f"**{event['resume_id']}**: {event['error']}")

# ── Search tab ────────────────────────────────────────────────────────────────
with search_tab:
    st.header("Search Resumes")

    if collection_count() == 0:
        st.warning("No resumes ingested yet — run ingestion first.")
        st.stop()

    query = st.text_input("Question", placeholder="e.g. Which Python developers have machine learning experience?")
    top_k = st.slider("Number of results", min_value=1, max_value=10, value=5)

    if st.button("Search & Ask", type="primary"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Searching…"):
                try:
                    hits = search(
                        query,
                        top_k=top_k,
                        allowed_categories=policy["allowed_categories"],
                    )
                    st.session_state["search_results"] = hits
                except Exception as e:
                    st.error(f"Search failed: {e}")
                    hits = []

            if hits:
                try:
                    st.write_stream(answer_stream(query, hits, role=role))
                    source_ids = list(dict.fromkeys(r["resume_id"] for r in hits))
                    st.caption(f"Sources: {', '.join(source_ids)}")
                except Exception as e:
                    st.error(f"Q&A failed: {e}")

    results = st.session_state.get("search_results", [])
    if results:
        st.subheader(f"Results ({len(results)})")
        for i, r in enumerate(results, 1):
            display_text = redact(r["text"], role)
            with st.expander(f"#{i} — {r['resume_id']} · {r['category']} · distance: {r['distance']}"):
                st.write(display_text)

# ── Analytics tab ─────────────────────────────────────────────────────────────
with analytics_tab:
    st.header("Analytics")

    allowed = policy["allowed_categories"]

    if resume_count(allowed_categories=allowed) == 0:
        st.warning("No resumes ingested yet — run ingestion first.")
        st.stop()

    if allowed:
        st.info(f"**{role}** — scoped to: {', '.join(allowed)}")

    # Controls
    categories = get_categories(allowed_categories=allowed)
    col1, col2 = st.columns([2, 1])
    with col1:
        category_options = ["All"] + categories
        selected = st.selectbox("Category", category_options)
        category_filter = None if selected == "All" else selected
    with col2:
        top_n = st.slider("Top skills", min_value=5, max_value=50, value=20)

    st.divider()

    # Chart 1 — Skill frequency
    st.subheader("Top Skills")
    freq = skill_frequency(category_filter, top_n, allowed_categories=allowed)
    if freq:
        skills, counts = zip(*reversed(freq))
        fig_skills = go.Figure(go.Bar(
            x=list(counts), y=list(skills),
            orientation="h",
            marker_color="steelblue",
        ))
        fig_skills.update_layout(
            xaxis_title="Frequency", yaxis_title="",
            margin=dict(l=0, r=0, t=10, b=0),
            height=max(300, top_n * 22),
        )
        st.plotly_chart(fig_skills, use_container_width=True)
    else:
        st.info("No skill data available for this selection.")

    st.divider()

    col_pie, col_hist = st.columns(2)

    # Chart 2 — Seniority distribution
    with col_pie:
        st.subheader("Seniority Distribution")
        seniority = seniority_distribution(category_filter, allowed_categories=allowed)
        fig_pie = go.Figure(go.Pie(
            labels=list(seniority.keys()),
            values=list(seniority.values()),
            hole=0.35,
            marker_colors=["#4CAF50", "#2196F3", "#FF9800"],
        ))
        fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=350)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.caption("Junior: 0–2 yrs · Mid: 3–6 yrs · Senior: 7+ yrs")

    # Chart 3 — Experience histogram
    with col_hist:
        st.subheader("Years of Experience")
        exp_vals = experience_values(category_filter, allowed_categories=allowed)
        fig_hist = go.Figure(go.Histogram(
            x=exp_vals, nbinsx=20,
            marker_color="steelblue", opacity=0.8,
        ))
        fig_hist.update_layout(
            xaxis_title="Years", yaxis_title="Resumes",
            margin=dict(l=0, r=0, t=10, b=0),
            height=350,
        )
        st.plotly_chart(fig_hist, use_container_width=True)
