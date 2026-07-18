# ComplianceHub — GRC Control Mapping & Reporting Toolkit

ComplianceHub is a full-stack Governance, Risk, and Compliance (GRC) toolkit designed for security engineers and compliance analysts. It unifies control mapping (e.g., CIS Controls v8), risk register management, and automated policy generation around a single relational database. 

Most GRC processes are tracked in disconnected spreadsheets resulting in drift between controls, risk findings, and policy documentation. ComplianceHub solves this by acting as a single source of truth, automating the generation of professional-grade gap assessment and policy documents directly from the database.

## Key Features

- **Control Mapping Tracker**: Maps organizational controls to real frameworks (e.g., CIS Controls v8) and tracks assessment status and evidence.
- **Interactive Assessment Engine**: A CLI-based interactive walkthrough to assess control implementations as Met, Partial, or Not Met with justification.
- **Risk Register**: Logs findings directly against specific controls, automatically scoring risk based on likelihood and impact matrices.
- **Automated Reporting**: Generates styled HTML reports for Gap Assessments and Risk Registers, ready for stakeholder review.
- **Policy Generator**: Dynamically generates security policies that automatically cross-reference and cite the specific framework controls they satisfy.

## Architecture

```text
CLI (Click) ──┬── Control DB (SQLite) ── shared source of truth
              │        ↑↓
              ├── Risk Register module ── writes findings linked to control IDs
              ├── Assessment module ── walks controls, records Met/Partial/Not-Met
              └── Report Generator (Jinja2)
                       ├── Gap Assessment HTML Report
                       ├── Risk Register HTML Report
                       └── Policy documents (auto-cites linked controls)
```

## Technology Stack
- **Backend:** Python 3.11, Click (CLI), SQLAlchemy (ORM), SQLite (Database)
- **Reporting:** Jinja2 (HTML/Markdown Templating), Markdown
- **Data Analysis:** Pandas (for data manipulation/export)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NisargV22/ComplianceHub.git
   cd ComplianceHub
   ```

2. **Install the package and dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -e .
   ```

## Quick Start & Usage

### 1. Initialize the Database
Seed the database with the default framework (CIS Controls v8) and set your organization profile.
```bash
compliancehub init --framework cis-v8 --company "Acme Corp"
```

### 2. Run an Assessment
Start the interactive assessment walkthrough to record control status (Met, Partial, Not Met) and rationale.
```bash
compliancehub assess --interactive
```

### 3. Manage the Risk Register
Log a risk finding tied directly to a control ID (e.g., `IA-5`). The risk score is automatically calculated.
```bash
compliancehub risk add --finding "No MFA on privileged accounts" --control IA-5 --likelihood high --impact high
```

List open findings:
```bash
compliancehub risk list
```

### 4. Generate Reports
Automatically generate beautifully formatted reports using your assessment data and risk findings.

Generate the Gap Assessment:
```bash
compliancehub report gap-assessment --output acme_gap_report.html
```

Generate the Risk Register:
```bash
compliancehub report risk-register --output acme_risk_register.html
```

Generate a targeted Security Policy (e.g., Password Policy mapping to specific controls):
```bash
compliancehub report policy --template password_policy --controls AC-2,IA-5 --output password_policy.html
```
*(All generated HTML reports can be opened directly in any modern web browser).*

## License
MIT License