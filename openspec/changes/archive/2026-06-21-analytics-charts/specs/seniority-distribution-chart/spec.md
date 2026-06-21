## ADDED Requirements

### Requirement: Seniority distribution pie chart
The system SHALL bucket resumes by `years_exp` into three seniority levels and render a pie chart: Junior (0–2 years), Mid (3–6 years), Senior (7+ years).

#### Scenario: Chart renders with data
- **WHEN** the Analytics tab is opened and resumes are ingested
- **THEN** the system SHALL display a pie chart with three slices labelled Junior, Mid, Senior showing percentage and count

#### Scenario: Category filter applied
- **WHEN** the user selects a category from the dropdown
- **THEN** the pie chart SHALL reflect seniority distribution for that category only

#### Scenario: All resumes have years_exp = 0
- **WHEN** all ingested resumes have unknown experience (years_exp = 0)
- **THEN** the pie chart SHALL show 100% Junior and a note that experience data may be incomplete
