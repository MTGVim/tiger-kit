# Jira

- Confirm the target surface only when it materially changes the draft. Jira Cloud REST API v3 comment bodies use Atlassian Document Format (ADF); Jira Server/Data Center and legacy integrations can use different formatting paths, including Wiki Markup. Do not assume raw Markdown will render as intended.
- For an ordinary copyable comment, use a few short connected paragraphs without headings. State the concrete behavior and the question or review request. Number separate questions only when that makes distinct answers easier to give; avoid report sections and unnecessary nesting or tables.
- Describe the relevant evidence or action in the comment. Do not add code or other source links by default; include the relevant issue link only when useful, and follow the main skill evidence-link rule for other links, including its contradiction exception.
- State the issue key and relevant current status only when verified. Include the evidence needed to answer or close each request.
- Use a person mention only when the intended Jira account is verified and the destination can resolve it. Do not invent mention syntax or account identifiers.

## Official references

- [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
- [About Atlassian Document Format and Wiki Markup](https://developer.atlassian.com/platform/framework/adf-builder/technical/about-adf/)
