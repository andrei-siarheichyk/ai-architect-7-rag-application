### Requirement: Category-scoped retrieval per role
The system SHALL apply a ChromaDB metadata filter restricting retrieved chunks to role-permitted categories. Roles with `allowed_categories: None` SHALL receive unfiltered results.

#### Scenario: HR retrieves across all categories
- **WHEN** an HR user searches for any query
- **THEN** results SHALL include chunks from all 24 categories

#### Scenario: Hiring Manager retrieves Engineering and IT only
- **WHEN** a Hiring Manager searches for any query
- **THEN** results SHALL only include chunks from the "Engineering" and "Information-Technology" categories

#### Scenario: Recruiter retrieves across all categories
- **WHEN** a Recruiter searches for any query
- **THEN** results SHALL include chunks from all 24 categories

### Requirement: Analytics scoped to allowed categories
The system SHALL scope all Analytics tab charts (skill frequency, seniority distribution, experience histogram) to role-permitted categories.

#### Scenario: Hiring Manager analytics scoped to Engineering and IT
- **WHEN** a Hiring Manager opens the Analytics tab
- **THEN** all three charts SHALL only reflect data from Engineering and Information-Technology resumes

#### Scenario: HR and Recruiter see full analytics
- **WHEN** HR or Recruiter opens the Analytics tab
- **THEN** charts SHALL reflect data from all categories (subject to any category dropdown filter the user applies)
