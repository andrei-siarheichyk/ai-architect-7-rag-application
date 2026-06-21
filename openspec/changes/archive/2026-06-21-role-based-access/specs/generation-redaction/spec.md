## ADDED Requirements

### Requirement: PII redaction for Recruiter role
The system SHALL strip personally identifiable information from resume chunk text before it is included in the LLM prompt, for roles with `redact_pii: True` (Recruiter). Redacted patterns SHALL include: email addresses, phone numbers, and street addresses.

#### Scenario: Email redacted from Recruiter prompt context
- **WHEN** a Recruiter submits a Q&A question and a retrieved chunk contains an email address
- **THEN** the email SHALL be replaced with `[EMAIL REDACTED]` in the LLM context

#### Scenario: Phone number redacted from Recruiter prompt context
- **WHEN** a Recruiter submits a Q&A question and a retrieved chunk contains a phone number
- **THEN** the phone number SHALL be replaced with `[PHONE REDACTED]` in the LLM context

#### Scenario: HR and Hiring Manager see unredacted context
- **WHEN** an HR or Hiring Manager user submits a Q&A question
- **THEN** chunk text SHALL be passed to the LLM without modification

### Requirement: Redaction applied to search result display
The system SHALL also redact PII from the chunk text displayed in the Search results UI for roles with `redact_pii: True`, not only in the LLM prompt.

#### Scenario: Recruiter search results show redacted text
- **WHEN** a Recruiter views search result snippets
- **THEN** email addresses and phone numbers SHALL appear as `[EMAIL REDACTED]` and `[PHONE REDACTED]`
