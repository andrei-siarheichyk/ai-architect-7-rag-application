### Requirement: Years of experience histogram
The system SHALL render a histogram of `years_exp` values across ingested resumes, showing how experience is distributed.

#### Scenario: Chart renders with data
- **WHEN** the Analytics tab is opened and resumes are ingested
- **THEN** the system SHALL display a histogram with years_exp on the x-axis and resume count on the y-axis

#### Scenario: Category filter applied
- **WHEN** the user selects a category from the dropdown
- **THEN** the histogram SHALL reflect experience distribution for that category only
