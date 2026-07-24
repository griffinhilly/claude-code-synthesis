# Verify After Bulk Agent Generation

After every batch of agent-generated files, run an automated quality gate before proceeding. The check should be fast (< 30s) and catch the common Haiku failure modes.

**Why:** In one bulk-generation session, Haiku agents produced placeholder content ("Concept A" multiple-choice answers), template-injected questions, empty directories, and malformed YAML. These are expected failure modes of bulk generation, not surprises. The process lacked an automated detection step between generation and the next action.

**How to apply:**
- After agents complete, before doing anything else, run a quick validation: files exist? frontmatter parses? core content > 100 chars? no placeholder patterns? no duplicate content across files?
- Build this into the workflow as a standard step, not an afterthought.
- Detection is the gap, not judgment — once issues are found, the fix process works well.

The pattern: generate → validate → fix-or-regenerate → next step. Skipping the validate step means the next step compounds on bad data, which costs more to unwind than the validation costs to run.
