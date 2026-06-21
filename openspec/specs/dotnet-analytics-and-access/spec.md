### Requirement: LINQ-based analytics aggregations
The system SHALL compute skill frequency, seniority distribution, and years-of-experience values from LiteDB using LINQ, scoped to role-allowed categories.

#### Scenario: Skill frequency returns top-N skills
- **WHEN** `Aggregator.SkillFrequency(topN: 10, allowedCategories: null)` is called
- **THEN** it SHALL return the 10 most frequent skills across all resumes as `List<(string Skill, int Count)>`

#### Scenario: Aggregation scoped to allowed categories
- **WHEN** `allowedCategories` is `["ENGINEERING"]`
- **THEN** only resumes with `Category == "ENGINEERING"` SHALL contribute to the aggregation

#### Scenario: Seniority buckets
- **WHEN** `Aggregator.SeniorityDistribution()` is called
- **THEN** it SHALL return `Dictionary<string, int>` with keys Junior (0–2 yrs), Mid (3–6 yrs), Senior (7+ yrs)

### Requirement: Role-based access policy
The system SHALL define a static `Policy` class with a `POLICIES` dictionary and `Redact(text, role)` method, equivalent to `policy.py`.

#### Scenario: Get policy for known role
- **WHEN** `Policy.Get("Recruiter")` is called
- **THEN** it SHALL return `AllowedCategories: null, RedactPii: true`

#### Scenario: Redact PII for Recruiter
- **WHEN** `Policy.Redact(text, "Recruiter")` is called with text containing an email
- **THEN** the email SHALL be replaced with `[EMAIL REDACTED]`

#### Scenario: No redaction for HR
- **WHEN** `Policy.Redact(text, "HR")` is called
- **THEN** the text SHALL be returned unchanged

### Requirement: Console menu with role switching
The system SHALL present a console menu allowing the user to select: Ingest / Search / Ask / Analytics / Switch Role / Exit. The active role SHALL be displayed in the menu header.

#### Scenario: Role switch takes effect immediately
- **WHEN** user selects "Switch Role" and picks "Hiring Manager"
- **THEN** all subsequent search and analytics operations SHALL use the Hiring Manager policy
