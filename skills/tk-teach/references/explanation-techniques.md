# Explanation Technique Reference

Read only the entries selected by explanation-routing.md. Shared offline HTML, citation, accessibility,
evidence, and document-shell rules remain in html-output.md.

## 01. Five-Step Ladder
- Use when beginners and practitioners need the same document at different depths.
- Start with one sentence and no jargon. Add no more than one new term at each step. Make every step
  independently understandable.
- Avoid for a mechanism whose timing is essential; the ladder has no timeline by itself.

## 02. Hands-on Simulator or Calculator
- Use when changing one input should change a numeric or behavioral result.
- Limit controls to one to three variables. Derive the drawing, values, and explanation from one
  pure model. Begin from a sourced value or an explicitly labeled illustrative baseline.
- Name the simplifications and assumptions. Do not present a model value as a measurement. Avoid
  when the topic has no meaningful variable to change.

## 03. Real Output
- Use when the actual output, log, response, or generated artifact is visible in the sources.
- Show source output. Label any shortened excerpt as a summary.
- Define unfamiliar terms before they block understanding. Never fabricate output.

## 04. Zine Comic
- Use when an idea can be divided into a small number of visual panels.
- Give each panel one idea and keep dialogue to a few lines. Use 1px panel rules.
- Avoid long sequences; more than six panels can be hard to scan.

## 05. Scrollytelling
- Use when a process changes state in a meaningful order.
- Keep the diagram stable and explain one or two sentences per step. The initial diagram state must
  match the first step.
- Provide a static step table when JavaScript is unavailable. Avoid excessive empty space.

## 06. Misconception Correction
- Use when a common misconception materially changes how readers understand or operate something.
- State a plausible misconception, mark it with text and strikethrough, then correct it with evidence.
  Explain what part was partly true when that matters.
- The section must still provide the basic mechanism. Do not invent a misconception.

## 07. Group Chat
- Use when several actors hand work to one another and their order matters.
- Write short natural turns with reactions and chat bubbles. Label time boundaries when timing is
  supported by evidence. Finish with a concise role summary when the conversation is long.
- Keep definitions findable; precise facts and evidence may sit beside the conversation. Distinguish
  observed times from illustrative scenarios.

## 08. Sketch Comedy
- On request only.
- Use for repeated, plausible misconceptions that can be corrected by another character with evidence.
- Avoid for mechanisms that need a precise diagram or extensive technical detail.

## 09. Socratic Questions
- Use when readers can derive a principle from a motivating problem.
- Ask a focused question before revealing the answer. Keep the derivation short and grounded.
- Avoid for facts that must be recalled exactly, such as a header name or threshold value.

## 10. Incident Postmortem
- Use when practical failure analysis is the clearest route to understanding.
- Label fictional events, values, and identifiers as illustrative. Follow symptoms, timeline, cause,
  and response in that order.
- Do not invent remedies unsupported by sources.

## 11. Illustrated Intuition
- Use to give an initial mental picture of a new concept.
- Use one analogy per scene, state its boundary in the same scene, and connect it back to the actual
  terms and mechanism.
- Avoid when the analogy hides details that are central to the claim.

## 12. Choose-Your-Own Path
- Use when a real policy or decision leads to different outcomes depending on a choice.
- Make every outcome reachable by native links without JavaScript and compare each outcome with the
  verified facts.
- Avoid if there is no genuine choice or if branches imply unsupported facts.

## 13. Sequence Diagram
- Use when three or four actors exchange messages in a known order.
- Give each actor a lane, put messages in reading order, and split materially different situations
  into separate scenes.
- Vertical distance does not represent time unless a scale says so; state wait duration separately.

## 14. Waterfall Timeline
- Use when elapsed time, overlap, or waiting is central.
- Put units and one sentence on how to read the axis above the figure.
- Explain the notation for readers who may not know waterfall charts.

## 15. Before/After Comparison
- Use when the contrast between two states is the conclusion.
- Show both states on the same time scale. Keep the comparison aligned and label the changed
  condition.
- Provide static snapshots without JavaScript. This comparison shows what changed, not necessarily
  why it changed.

## 16. Concept Map
- Use when many terms have meaningful relationships.
- Label every arrow with the relationship and provide a table alternative.
- Avoid for time-ordered processes.

## 17. Infographic Poster
- Use as a whole-document structure only when the user asks for a one-page summary.
- Put the conclusion first and include a small set of key points.
- Preserve links to evidence; avoid compressing every reason into an unreadable poster.

## 18. Animated Metaphor
- Use when flow, capacity, or blockage can be represented accurately as motion.
- List the limits of the analogy. Respect reduced motion and provide a readable static state.
- Choose another technique if the list of limitations is longer or more important than the analogy.

## 19. Predict First
- Use when intuition is likely to diverge from the verified result.
- Ask for a prediction before revealing the answer. Explain why a plausible wrong prediction feels
  reasonable.
- Avoid when the reader lacks the prerequisites to make a meaningful prediction.

## 20. Quiz
- Use when a small set of core facts can be tested with immediate feedback.
- Keep answers collapsed until an explicit reveal and end with a concise recap.
- Do not use styling, order, or wording that leaks correctness. A standalone offline quiz is not
  secure against source inspection.

## 21. Flashcards
- Use when readers need to revisit a set of terms and definitions.
- Keep each card focused and operable by keyboard.
- Avoid when the relationships or process between terms matter more than recall.

## 22. Invent Before Reveal
- Use when a design solution follows step by step from a stated problem.
- Begin with the problem. Ask what constraint the next step must satisfy, then compare the derived
  design with its actual name and implementation.
- Reveal the real names before the end; readers cannot infer arbitrary terminology.

## 23. Feynman Technique
- On request only.
- Use a first explanation to reveal a gap, then repair that gap with evidence and a clearer second
  explanation. A reader exercise may ask them to explain from memory.
- Do not claim that self-explanation research alone proves this is a universally effective reader
  format.

## 24. Hint Ladder
- Use when the reader should solve a diagnostic question independently.
- Reveal hints in order and provide a grounded final explanation.
- Avoid when the hints require knowledge the document has not introduced.

## 25. Cheat Sheet
- Use for formulas, settings, commands, or queries that readers will revisit.
- Group by task and include only sourced values.
- Pair with explanatory sections when readers also need to know why the items work.

## 26. Annotated Code
- Use when configuration or code is the central evidence.
- Align each explanation with the relevant code line or block and preserve exact identifiers.
- Use another view for timing and concurrent activity that code alone cannot show.

## 27. Terminal Replay
- Use when commands provide the clearest way to observe and diagnose a system.
- Show only real documented or captured output, with its source and context.
- Do not invent terminal output or replace a materially important output with an unsupported summary.

## 28. Failure Modes
- Use when an incorrect setting can fail quietly or create a distinct failure state.
- Organize by symptom and connect each one to its cause and a source-supported response.
- Do not supply a fix that the available evidence does not support.

## 29. Slide Deck
- Use as a whole-document structure when the user requests a presentation.
- Support keyboard navigation and leave all slides readable in document order without JavaScript.
- Retain the connecting explanation needed for a standalone reader.

## 30. Social Thread
- On request only.
- Make it a separate sharing summary, not a substitute for the full explanation.
- Do not imitate a named platform or account. Keep technical mechanisms in the full document.
