from collections import Counter

from tinydb import TinyDB, Query

from src.config import TINYDB_PATH

_SENIORITY_BUCKETS = {"Junior": (0, 2), "Mid": (3, 6), "Senior": (7, 999)}


def _load(category: str | None, allowed_categories: list[str] | None = None) -> list[dict]:
    db = TinyDB(str(TINYDB_PATH))
    docs = db.all()
    if allowed_categories:
        docs = [d for d in docs if d.get("category") in allowed_categories]
    if category:
        docs = [d for d in docs if d.get("category") == category]
    return docs


def get_categories(allowed_categories: list[str] | None = None) -> list[str]:
    db = TinyDB(str(TINYDB_PATH))
    cats = {doc["category"] for doc in db.all() if "category" in doc}
    if allowed_categories:
        cats = cats & set(allowed_categories)
    return sorted(cats)


def resume_count(allowed_categories: list[str] | None = None) -> int:
    db = TinyDB(str(TINYDB_PATH))
    docs = db.all()
    if allowed_categories:
        docs = [d for d in docs if d.get("category") in allowed_categories]
    return len(docs)


def skill_frequency(category: str | None = None, top_n: int = 20, allowed_categories: list[str] | None = None) -> list[tuple[str, int]]:
    """Return top-N (skill, count) pairs sorted by count descending."""
    docs = _load(category, allowed_categories)
    counter: Counter = Counter()
    for doc in docs:
        for skill in doc.get("skills", []):
            if skill:
                counter[skill.strip()] += 1
    return counter.most_common(top_n)


def seniority_distribution(category: str | None = None, allowed_categories: list[str] | None = None) -> dict[str, int]:
    """Bucket resumes by years_exp: Junior 0–2, Mid 3–6, Senior 7+."""
    docs = _load(category, allowed_categories)
    buckets = {label: 0 for label in _SENIORITY_BUCKETS}
    for doc in docs:
        exp = doc.get("years_exp", 0) or 0
        for label, (lo, hi) in _SENIORITY_BUCKETS.items():
            if lo <= exp <= hi:
                buckets[label] += 1
                break
    return buckets


def experience_values(category: str | None = None, allowed_categories: list[str] | None = None) -> list[int]:
    """Return raw years_exp values for histogram rendering."""
    docs = _load(category, allowed_categories)
    return [doc.get("years_exp", 0) or 0 for doc in docs]
