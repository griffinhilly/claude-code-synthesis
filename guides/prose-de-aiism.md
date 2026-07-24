# De-AI-ism Pass — Removing LLM Voice from User-Facing Prose

Purpose: a concrete catalog + method for stripping AI-tells from prose that humans will read (dashboard copy, published pages, reports, emails). Readers stop reading when they detect AI voice; the content doesn't get a chance. Origin: a dashboard voice pass on a published research site.

Companion rules that always apply alongside this guide:
- A hard ban on "It's not X, it's Y" / "X isn't Y, it's Z" constructions.
- Target register: a serious-but-conversational, accessibility-first, rigor-without-obscurity voice (think Scott Alexander / Matt Yglesias / Kelsey Piper register). The author publishes in THEIR OWN voice — this guide is for utility prose (site copy, captions, explainers), not for ghostwriting anyone's articles.

## The immutable-content rule (evidence-bearing text)

When the prose carries evidence claims (verdicts, hedges, numbers, caveats — anything review-hardened or pre-registered):
- Numbers, units, verdict strength, evidence tiers, and flags NEVER change.
- Hedge CONTENT never weakens. Hedge PHRASING may be humanized: "not detected at achievable power (not thereby ruled out)" can become "we couldn't detect this at the sample sizes available — which is different from showing there's none." Same epistemic content, human cadence.
- When unsure whether a rewrite preserves the claim, keep the original sentence and rewrite only around it.

## Tell catalog

**Contrast scaffolds (highest-priority tells):**
- "It's not X, it's Y" / "X isn't just Y, it's Z" (hard ban)
- "not just X — Y" / "not only X but also Y"
- "less about X, more about Y"
- Fix: state what it IS. If the contrast matters, give the context that makes it obvious.

**Fanfare verbs and empty operators:** delve, dive into, unpack, unlock, harness, leverage (as verb), navigate (metaphorical), foster, bolster, underscore, showcase, spearhead, "serves as," "stands as," "acts as," "plays a key role in," "marks a," "represents a." Fix: use the plain verb ("shows," "is," "runs," "uses") or delete.

**Grandiosity nouns/adjectives:** crucial, pivotal, essential, comprehensive, seamless, powerful, transformative, game-changing, landscape, tapestry, journey, treasure trove, myriad, plethora, "in today's ___ world." Fix: delete or replace with the specific fact that earned the adjective.

**Throat-clearing openers:** "It's worth noting that," "It's important to note," "Notably," "Importantly," "Interestingly," "At its core," "In essence," "Essentially," "Ultimately" (as filler), "That said." Fix: delete; start with the content.

**Structural tics:**
- Rule-of-three everywhere (triplet phrases in sentence after sentence). Break the rhythm: some lists of two, some of four, some sentences with one item.
- Every bullet opening with a **Bolded Lead-in:** followed by explanation. Fine in reference docs; a tell in prose surfaces. Vary or unbold.
- Em-dash overuse: no more than two per paragraph (as a rule of thumb); most can become commas, parens, or periods.
- Symmetric paragraphs (all ~4 sentences). Vary hard: one-sentence paragraphs are allowed.
- "The result? ..." rhetorical-fragment cadence; "And that's exactly the point." closers.
- Colon headlines ("X: Why Y Matters") when a plain headline works.
- Starting sentences with a referent-less "This" (name the thing).

**Empty intensifiers:** actually, very, just, truly, deeply, significantly (when not statistical), vast, incredibly. Almost always deletable.

**Agent-register leakage:** "load-bearing," "let me gently push back," "flag," "surface" (as verb), "artifact" (outside technical contexts), "leverage points," "here's the thing." These read as workflow jargon to outside readers.

**AI-politeness residue:** "feel free to," "please note," "simply," "you can easily."

## Crowd-sourced phrase inventory

Compiled from a widely-shared social-media thread on AI writing tells (dozens of contributors, ~40 phrases identified). Heavy on the chat/sycophancy register but several leak into expository prose. Top tiers:

- **Tier 1 (most-attested):** "load-bearing" (the dominant tell), "quietly" (softener adverb, often with "chaotic"), "genuinely" (standalone intensifier), "genuine tension," "sit with that."
- **Tier 2:** "doing the heavy lifting," "earns its keep," "gently push back," "genuinely good," "that is gold."
- **Tier 3 highlights:** "earns its place," "doing real work," "sharp observation," "you've identified something real," "you're absolutely right," "the flywheel," "[x] engine," "the brutal truth:", "that distinction matters," "land/landed" (as verb for ideas), starting sentences with "And,"/"But,".
- **Diagnostic rule from the thread:** single occurrences are weak evidence; *combinations* in one passage are near-certain (e.g., "load-bearing" + "genuinely" + any hedge-pivot). Sweep for stacks, not singletons.

## Compliance narration and instruction echo (high priority)

The deepest structural tell on informational pages: **the text narrates its own editorial rules instead of silently following them.** Real examples flagged on a public findings page — AFTER a full de-AI-ism pass, so treat these as what survives naive passes:

| AI (flagged) | Why it's a tell | Human fix |
|---|---|---|
| "No single row is 'the' recurrence rate; the range is the answer." | Instruction echo — the internal remediation rule pasted into copy; also strawman-then-correct (nobody claimed one row was "the" rate) | "How often does war come back? It depends on how you count: 46 to 69 percent of post-war decades see another conflict, depending on the dataset and definitions." |
| "Two caveats stay attached." | Mechanical caveat-freight metaphor ("stay attached," "carries," "ships with," "travels with") | "Two caveats:" — or weave them into the claim's own sentence. |
| "Everything on this page is a descriptive pattern in observational data." | Page describing itself; meta-framing opener | "These are patterns in the data, not proof of causes." |
| "Null results get the same careful wording as findings — 'we cannot detect an effect at this power,' never 'there is no effect' — and every claim links to its evidence tier..." | Full rulebook recital; quotes its own style constraints at the reader | Delete; demonstrate the discipline instead. At most, once: "Where we found nothing, we say so — and 'nothing' means the test couldn't see an effect, not that there is none." |

Tests to apply:
- **Instruction-echo test:** if a sentence could double as a line in the writing instructions or the pre-registration's decision rules, it does not belong in reader-facing copy.
- **Self-reference test:** any sentence whose subject is "this page," "this section," "every claim," "each finding" is narrating rather than saying. Rewrite so the subject is the world (countries, wars, incomes), not the document.
- **Strawman test:** a negation must negate something a reasonable reader actually believed. If the reader held no such prior, state the positive fact and delete the correction ceremony.

## Prose-minimization beats prose-polishing

On data-heavy pages, the reliable de-AI move is FEWER SENTENCES, not better ones. Headings, tables, and numbers don't have a voice problem. Every surviving sentence must do work a table or heading cannot. If a de-AI pass leaves the page at the same word count, it polished the tells instead of removing their habitat.

## The ceiling rule (voice-bearing passages)

Utility copy (captions, caveats, labels, table intros) can be de-AI'd by an agent. VOICE-BEARING passages — page openers, framing paragraphs, anything that sets the register for a published surface — hit a ceiling: an agent iterating toward "sounds human" is playing an imitation game it loses on inspection. The author should write what they publish. The correct workflow: (1) agent minimizes and de-tells the prose, (2) agent extracts the remaining voice-bearing passages into a numbered handoff list (current text + one line stating the immutable content each must convey), (3) the author rewrites those few passages in their own words, (4) agent wires them in verbatim. Ten minutes of the author's own writing beats ten rounds of imitation.

## Underlying patterns (why the phrase lists keep growing)

Two conceptual tells that survive any phrase-list update — drawn from bookmarked commentary threads on LLM writing style:

1. **Valueless negation.** The deep form of "it's not X, it's Y": sentence after sentence negates a prior the reader never held — offering something, negating it, swerving away. The text keeps implying you believed something wrong so it can correct you. Fix: assert the positive claim; delete the phantom prior.
2. **Modular writing / uniform semantic weight.** Every sentence written as if it will be evaluated in isolation — fully self-contained, no dependence on its neighbors, no minor self-reference, importance spread evenly. Human prose is "semantically turbulent": some sentences carry the load, others just connect; later sentences lean on earlier ones. Fix: let sentences depend on context; vary how much each one carries; refer back casually ("that gap," "the same problem") instead of restating.

## Method

1. **Read-aloud test.** Would a knowledgeable person say this sentence to a colleague? If it sounds like a press release or a report-generator, rewrite in the words they'd actually say.
2. **Delete first, replace second.** Most tells are removable with zero information loss. Deletion beats synonym-swapping (a swapped tell is still a tell).
3. **Concrete subjects, concrete verbs.** "Escape rates fall the longer a country stays poor" beats "the analysis reveals a pronounced decline in escape propensity." Name the actor; use the verb the actor performs.
4. **Vary sentence length.** AI prose has a metronome. Follow a long sentence with a short one. Fragments are legal.
5. **One idea per sentence in explainer prose.** If a sentence has three commas and a semicolon, it's probably three sentences.
6. **Plain register is not dumbing down.** Keep technical terms that carry precision (hazard, FDR, pre-registration); cut ceremony around them. The standard: a smart reader with no domain background follows every sentence without slowing down.
7. **Final pass: count survivors.** Grep the catalog terms; every survivor needs a reason (quoted material, technical usage, deliberate emphasis).

## When this guide fires

- Any user-facing prose written or revised by an agent (site copy, README-for-humans, report text, published explainers).
- Whenever anyone says text "reads AI," "sounds like ChatGPT," or "has LLM voice."
- As a named final pass in content build-outs — run it BEFORE showing the human, not after they complain.
