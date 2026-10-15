# Jira

- Confirm the target surface only when it materially changes the draft. Jira Cloud REST API v3 comment bodies use Atlassian Document Format (ADF); Jira Server/Data Center and legacy integrations can use different formatting paths, including Wiki Markup. Do not assume raw Markdown will render as intended.
- For an ordinary copyable comment draft, prefer a short context paragraph, numbered questions and a clear description of the evidence or action that would settle each question. Keep nesting and tables simple unless the destination has been checked.
- State the issue key and relevant current status only when verified. Include the evidence needed to answer or close each request.
- Use a person mention only when the intended Jira account is verified and the destination can resolve it. Do not invent mention syntax or account identifiers.

## Official references

- [Jira Cloud REST API v3](https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/)
- [Atlassian Document Format](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/)
- [About Atlassian Document Format and Wiki Markup](https://developer.atlassian.com/platform/framework/adf-builder/technical/about-adf/)
