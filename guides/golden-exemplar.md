# Golden Exemplar Method

When creating a new skill, refining an existing one, or building something in an unfamiliar domain, use this method to extract quality from existing work rather than inventing from scratch.

## When to Use
- Building a new skill or slash command
- Entering an unfamiliar technical domain
- Wanting to level up the quality of an existing tool/script/workflow
- The user asks "how should we approach X?" and a great example exists

## Process

### 1. Find the Exemplar
Identify a project, repo, or artifact that does what you're trying to generalize — at a high level of quality and sophistication. Sources:
- **Open source repos** — clone to `/tmp/` and study
- **User's own past work** — search past sessions or project history for relevant examples
- **The user's bookmarks or saved references** — search for relevant content if available
- **The user** — ask: "Do you know of any repos or projects that do something similar?"

### 2. Study It Deeply
Don't skim — investigate thoroughly:
- Read the architecture, not just the surface API
- Understand *why* it works, not just *what* it does
- Identify the design principles that make it good (not the implementation details)
- Note what makes it agent-ergonomic vs. human-ergonomic

### 3. Extract Principles
Generalize from the specific to the abstract:
- What patterns recur across the best parts?
- What constraints did the exemplar respect that made it robust?
- What would a model need to know to reproduce this quality in a different domain?

### 4. Encode into Skill/Guide
Write the extracted principles into the target skill or guide:
- Lead with principles, not implementation steps
- Include concrete examples from the exemplar (the model generalizes better from real examples)
- Use progressive disclosure — top-level summary, then details on demand
- Test: could an agent with only this skill produce exemplar-quality output?

### 5. Validate via Application
Apply the new/refined skill to a real project and compare quality against the exemplar. Iterate if the gap is too large.

## Anti-Patterns
- Copying implementation details instead of principles
- Studying only one exemplar (study 2-3 if available for better generalization)
- Skipping the "why" and encoding only the "what"
- Making the skill so specific to the exemplar that it doesn't generalize
