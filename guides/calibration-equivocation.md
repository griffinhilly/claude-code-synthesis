# Calibration Equivocation — Force Disambiguation

When evaluating plans that use "calibrate," "calibration," "tune," "validate," or "fit" in a Bayesian / IRT / Rasch / adaptive-learning / fluency / mastery / psychometric / econometric context, force the disambiguation: *which* calibration?

The same word routinely covers two completely different operations with wildly different cost curves:

1. **Topology verification** — does the prereq edge / graph relationship exist? Does the upstream-walk make pedagogical sense? Manual review by an expert. A few dozen topics in a few weeks is honest scope.

2. **IRT / Rasch item-difficulty calibration** — what is the b-parameter for this question under this learner's θ? Requires learner-response data on items under known prior-knowledge state. Tens of responses per topic minimum. A meaningfully sized topic × learner grid is months of recruitment + analysis.

**Why:** Discovered during a parent-acquisition dialectic for an education product. Both a content-engine advocate and a product-features advocate were trading on "calibration" as a rhetorical bridge. Content side: "N videos = N calibrated topics" (only topology, not psychometrics). Product side: "a multi-week calibration sprint with dozens of learners across a large topic spine" (a thin response count per topic even at the upper end). **Both referees independently flagged the equivocation; it was the most devastating single landing in the dialectic.**

**How to apply:** Any time a plan, advocate, or agent uses calibration-language in the relevant context, force the disambiguation. Honest short-timeline deliverables for a solo-engineer project look like topology verification on a narrow surface, not psychometric calibration of a meaningful item bank. Plans that promise the latter in under a couple months are overclaiming.

Applies to any project involving adaptive assessment or psychometric inference. The distinction also generalizes loosely to credence-calibration discussions in other domains, and to econometric "calibration" / "tuning" / "fitting" contexts — different operations again, but the equivocation pattern is the same shape (using one word for substantively different epistemic operations).
