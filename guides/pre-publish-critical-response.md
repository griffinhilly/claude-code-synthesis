# Pre-Publish Critical Response Audit

Before publishing content for an external audience — articles, blog posts, tweet threads, ledger entries that will go public, working papers, claude-code-synthesis updates — generate 10–15 plausible critical responses from the *target* audience first. Address the valid ones in the content. Note the invalid ones for later reference but don't pre-emptively defend against them in-text.

**Why:** First-impression critical responses are predictable, and the strongest critics will land them publicly if the author doesn't land them first. Pre-empting valid criticism strengthens the piece; pre-empting invalid criticism dilutes it. The act of generating the responses also reveals which claims in the draft are weakest — those are the ones most worth tightening before going live.

**How to apply:**
1. Identify the target audience explicitly. Different audiences raise different criticisms; "general readers" is too vague to produce useful predictions.
2. Generate 10–15 critical responses, ideally via parallel sub-agents reading the draft from different lenses (skeptic, domain expert, hostile audience member, friendly audience member who's confused).
3. Sort the responses: VALID (address in content) / INVALID (note for reference) / EDGE (decide based on stakes).
4. Address VALID criticisms by either revising claims, adding caveats, or pre-empting in a "what about X" section. The point is the criticism doesn't *successfully* land later — not that it never gets raised.
5. The "argue the opposite" rule (CLAUDE.md) is the per-claim version of this; the pre-publish audit is the per-piece version.

**When to skip:** Internal-only writing (project notes, MEMORY.md updates, draft scaffolds) where the author *is* the audience. The cost-benefit only earns its place when there's a real external audience and a piece long enough that critical-response generation produces 10+ distinct attacks.

**Adjacent rules:** writing-style feedback docs (voice), CLAUDE.md "Argue the opposite before committing" (per-claim version), a virality/critical-lens guide if one exists in your setup (which lens to use).
