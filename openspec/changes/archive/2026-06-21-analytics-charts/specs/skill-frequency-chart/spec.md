## ADDED Requirements

### Requirement: Skill frequency bar chart
The system SHALL aggregate skill counts from TinyDB and render a horizontal bar chart of the top-N most frequent skills, optionally filtered by job category.

#### Scenario: Chart renders with data
- **WHEN** the Analytics tab is opened and resumes are ingested
- **THEN** the system SHALL display a horizontal bar chart of the top 20 skills by frequency across all resumes

#### Scenario: Category filter applied
- **WHEN** the user selects a category from the dropdown
- **THEN** the chart SHALL update to show skill frequencies for that category only

#### Scenario: No resumes ingested
- **WHEN** TinyDB contains no documents
- **THEN** the system SHALL display a warning instead of a chart

### Requirement: Configurable top-N
The system SHALL provide a slider to configure how many top skills to display, defaulting to 20 with a range of 5–50.

#### Scenario: User adjusts top-N slider
- **WHEN** the user sets the slider to 10
- **THEN** the chart SHALL show exactly 10 skills
