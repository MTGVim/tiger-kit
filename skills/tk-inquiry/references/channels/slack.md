# Slack

## Draft shape

- For a DM or thread reply, use a few short connected paragraphs in the requester's established voice. Give the minimum context and evidence before the ask; omit headings, bold section labels and bullets by default. Use a short list only when several independent answers need separating.
- If the source discussion is in a thread, read that thread before drafting and write a reply suited to it.
- Use inline code formatting for identifiers, enum and status values, API paths, filenames, record IDs and short log excerpts. Describe the behavior first and put any needed code identifier in parentheses. Use a code block only for longer snippets.

## Formatting and mentions

- Slack's composer supports bold, italics, strikethrough, code, code blocks, quotes and ordered or bulleted lists. Its markup preference uses `*bold*`, `_italic_`, `~strikethrough~`, backticks and fenced code blocks. The default composer may apply formatting through its toolbar, so do not assume copied markup will render the same way in every workspace.
- Avoid report-style headings and decorative lead-in markers. Do not add links to code or evidence unless the user asks for them.
- Write numeric ranges with a hyphen, such as `3-5`. In markup mode, tildes delimit strikethrough text.
- Include a mention only for a verified member or group. A name must resolve to the intended entry in Slack's autocomplete; when it is ambiguous or unverified, leave `[select recipient in Slack]` and tell the user to choose the exact entry before sending.

## Official references

- [Format your messages with markup](https://slack.com/help/articles/360039953113-Format-your-messages-in-Slack-with-markup)
- [Use mentions in Slack](https://slack.com/help/articles/205240127-Use-mentions-in-Slack)
