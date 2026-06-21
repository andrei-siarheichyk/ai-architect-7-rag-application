## ADDED Requirements

### Requirement: Role selector in sidebar
The system SHALL display a dropdown in the Streamlit sidebar allowing the user to select one of three roles: HR, Hiring Manager, Recruiter. The selected role SHALL be stored in `st.session_state["role"]` and persist across tab switches within the same browser session.

#### Scenario: Default role on first load
- **WHEN** the app loads for the first time
- **THEN** the role SHALL default to "HR"

#### Scenario: Role switch takes effect immediately
- **WHEN** the user selects a different role from the sidebar dropdown
- **THEN** all subsequent search, Q&A, and analytics operations SHALL use the newly selected role's policy

#### Scenario: Active role displayed
- **WHEN** any tab is active
- **THEN** the sidebar SHALL clearly show which role is currently active
