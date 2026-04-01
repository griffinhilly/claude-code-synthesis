# Review Dimensions

Check the appropriate dimensions based on work type.

## For Code
1. Does it meet the stated success criteria?
2. Does it follow project conventions (from CLAUDE.md)?
3. Are there bugs, edge cases, or error handling gaps?
4. Is it simple and focused, or over-engineered?
5. Are there security issues (SQL injection, hardcoded credentials, etc.)?
6. Would a future agent be able to understand and modify this code? (agent-first check)

## For Data / Analysis
1. Do the numbers make sense? Sanity check key values against known baselines.
2. Are there data quality issues (nulls, duplicates, unexpected ranges)?
3. Do visualizations accurately represent the data?
4. Are conclusions supported by the evidence? Could the opposite conclusion be argued?
5. Were all data sources actually consulted, or were some assumed/skipped?
6. Are counts and references in COMP files consistent with actual data?
7. **Claim-Evidence table:** For each factual claim in the output, cite the specific evidence (query result, cell value, test output). Claims without evidence are flagged as unverified. Positive claims ("the model works," "data is clean") require stronger evidence than negative claims — confirmation is cheaper to fake than disconfirmation.
8. **Forcing specificity:** For any generalized claim ("teams that X tend to Y"), name a specific instance. If no concrete example can be cited, the claim is unsupported abstraction. For statistical claims, name the data point that best and worst fits the pattern.

7. **Claim-Evidence table:** For each factual claim in the output, cite the specific evidence (query result, cell value, test output). Claims without evidence are flagged as unverified.
8. **Asymmetric evidence bar:** Positive claims ("the model works," "data is clean") require stronger evidence than negative claims ("this approach failed"). Confirmation is cheaper to fake than disconfirmation.
9. **Forcing specificity:** For any generalized claim ("teams that X tend to Y"), name a specific instance. If no concrete example can be cited, the claim is unsupported abstraction. For statistical claims, name the data point that best and worst fits the pattern.

## For Writing / Content
1. Is it consistent with the project framework and voice?
2. Are claims supported? Would they survive the "argue the opposite" test?
3. Is the structure clear to the target audience?
4. Does it pass the "would this embarrass me" test — if handed to the reader as-is?

## Cross-Model Review (for high-stakes work)
For statistical analysis, architectural decisions, or anything where confirmation bias is a risk: suggest running the review through a second model (ChatGPT/Gemini) independently and comparing conclusions.
