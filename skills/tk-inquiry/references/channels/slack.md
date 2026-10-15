# Slack

## Draft shape

- Put the request in the opening lines, then add the minimum context and evidence needed to answer.
- Use short paragraphs and bullets. If the source discussion is in a thread, draft a reply for that thread.
- Use inline code formatting for identifiers, enum and status values, API paths, filenames, record IDs and short log excerpts. Use a code block only for longer snippets.

## Formatting and mentions

- Slack's composer supports bold, italics, strikethrough, code, code blocks, quotes and ordered or bulleted lists. Its markup preference uses `*bold*`, `_italic_`, `~strikethrough~`, backticks and fenced code blocks. The default composer may apply formatting through its toolbar, so do not assume copied markup will render the same way in every workspace.
- Prefer bold lead-in lines and bullets over GitHub Markdown headings or tables unless the actual destination has been checked.
- Write numeric ranges with a hyphen, such as `3-5`. In markup mode, tildes delimit strikethrough text.
- Include a mention only for a verified member or group. A name must resolve to the intended entry in Slack's autocomplete; when it is ambiguous or unverified, leave `[select recipient in Slack]` and tell the user to choose the exact entry before sending.

## Official references

- [Format your messages with markup](https://slack.com/help/articles/360039953113-Format-your-messages-in-Slack-with-markup)
- [Use mentions in Slack](https://slack.com/help/articles/205240127-Use-mentions-in-Slack)
