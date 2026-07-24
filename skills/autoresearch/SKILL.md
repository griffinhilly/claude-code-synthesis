---
name: autoresearch
description: Bounded autonomous optimization loop with rollback. Agent iterates on code; human iterates on prompt. Numeric eval + wall-clock budget + git-branch commits + keep-or-revert. Use for any optimization problem with a measurable metric.
user-invocable: true
disable-model-invocation: false
argument-hint: --metric <fn> --budget <seconds> --prompt <path> --script <path> [--branch <name>] [--shape-budget <N>]
---

# /autoresearch — Bounded Autonomous Optimization Loop

A parameterized harness for autonomous metric-driven iteration. The agent proposes changes, runs them, measures, keeps the wins, reverts the losses, logs the result, repeats until budget exhausts.

**This skill unlocks a problem-class neither `/overnight` nor `/loop` reaches**: bounded autonomous optimization with revertability. Use when the work has the shape *"improve a measurable metric on a code artifact within a budget, with rollback."*

**Reference:** Karpathy's autoresearch pattern; @altryne (Shopify Liquid +53%); @witcheer (45 experiments/night); @aakashgupta (100+ ML experiments overnight); convergent pattern seen across a broader bookmark scan on this topic.

---

## Required Inputs (parameter contract)

Per CLAUDE.md "Skills as method-calls with parameters" — this skill is a process; the invocation supplies the world. **Refuse to run without all four primary parameters.**

| Param | Type | Description |
|---|---|---|
| `--metric <fn>` | Python callable path | Returns a numeric score. Must be deterministic. Higher = better (negate if you have an error/loss metric). |
| `--budget <seconds>` | Integer | Wall-clock budget. Use seconds, not steps/tokens. |
| `--prompt <path>` | Markdown file | The *human-iterated* artifact. The agent reads it but must not modify it. |
| `--script <path>` | Python file | The *agent-iterated* artifact. The agent edits and commits this. |
| `--branch <name>` | String (optional) | Feature branch for commits. Default: `autoresearch/<timestamp>` |
| `--shape-budget <N>` | Integer (optional) | Require ≥N structurally different approaches before declaring done (depth alongside breadth). Default: none. |

**Hard rejection rules** (refuse to start):
- No `--metric` callable — "improve this code" without a metric is not autoresearch, it's vibes.
- `--metric` is "ask Claude if output is better" without a fixed rubric and temperature=0 — that's narration in latent space, exactly the latent-vs-deterministic boundary violation (per CLAUDE.md). If using LLM-as-judge, the judge prompt + rubric must be fixed and committed.
- `--prompt` and `--script` not in a git repository — can't roll back without git.
- Current branch has uncommitted changes — refuse until working tree is clean (or user explicitly waives).

---

## Process

### Step 1: Validate inputs

Refuse with a clear message if any hard-rejection rule fires. Show the user the missing piece and a suggestion to fix it.

### Step 2: Establish baseline

1. Check out `--branch` (create if absent).
2. Run `--metric` on the current code → record as `baseline_score`.
3. Log to `experiments.jsonl` in the project root:
   ```json
   {"timestamp": "...", "kind": "baseline", "metric": <baseline_score>, "script_hash": "...", "prompt_hash": "..."}
   ```

### Step 3: Loop until budget exhausted

Each iteration:

1. **Propose** (latent): Read `--prompt` (the human's instructions on what to try) + current `--script` + recent `experiments.jsonl` entries. Propose a concrete change. The proposal must be *specific* (an exact diff or a precise behavioral change), not a general direction.
2. **Apply** (deterministic): Write the change to `--script` as a working-tree modification.
3. **Run** (deterministic): Execute the script + `--metric` callable. If the script crashes, record as a failed experiment (revert + log).
4. **Measure** (deterministic): Compute the new metric value.
5. **Decide** (deterministic):
   - If `new_score > best_score_so_far`: `git add --script && git commit -m "<diff summary> | metric: <new_score>"` → update `best_score_so_far` → keep
   - Else: `git reset --hard HEAD` → revert
6. **Log** (deterministic): Append to `experiments.jsonl`:
   ```json
   {"timestamp": "...", "iteration": N, "proposal": "<one-line summary>", "metric": <score>, "decision": "kept"|"reverted", "notes": "<optional>"}
   ```
7. **Check budget**: If `(time.time() - start) > --budget` OR (if `--shape-budget` set and ≥N distinct approaches tried), exit loop.

### Step 4: Emit summary

When the loop exits, write a Markdown summary to `autoresearch_summary_<timestamp>.md` in the project:

- Baseline metric → best metric achieved (delta)
- Total iterations attempted; kept vs reverted ratio
- Top-3 experiments by metric delta, with proposal summary and diff
- Approaches tried (if `--shape-budget` was set, show diversity of approaches)
- Suggested next direction(s) based on what worked

Also report the summary in chat.

---

## Latent / Deterministic Split (explicit, per CLAUDE.md rule)

| Step | Latent / Deterministic | Notes |
|---|---|---|
| Propose change | **Latent** | Reading prompt + script + recent log; proposing next iteration is judgment |
| Apply change to file | Deterministic | File write |
| Run script + metric | Deterministic | Subprocess call |
| Measure score | Deterministic | Function returns a float |
| Decide keep/revert | Deterministic | `if new > best: keep else: revert` |
| Commit / reset | Deterministic | git commands |
| Log to experiments.jsonl | Deterministic | JSON append |
| Summary at end | Latent (mostly) | Synthesizing trend across runs; identifying what worked |

**The only latent steps are propose and summarize.** Everything else is plumbing. If the implementation puts deterministic work in latent space, the loop will produce non-reproducible results — the diagnostic test for whether autoresearch was implemented correctly is whether re-running the same loop with the same baseline produces the same trajectory (it should, modulo agent sampling on the propose step).

---

## When This Skill Triggers (use it for)

- **A predictive model's accuracy metric** (e.g. R² or classification accuracy on a held-out set) as the fitness function
- **Prompt/brief iteration for an internal tool** — quality rubric (committed prompt + temperature=0 LLM-as-judge) as metric
- **Regression fits across a panel dataset** — R² on regression targets as the metric
- **Prompt engineering on your own skills** — pass rate against `~/.claude/tools/skill-trigger-evals.py` JSONL
- **Forecasting/prediction-market work** — calibration / Brier score / log-loss as metric
- **Report-drafting pipelines** — readability score or human-rating rubric
- **Any latency / throughput optimization** — wall-clock or QPS as metric

**Don't use this for:**
- Open-ended exploration without a metric ("let's see what we can find") — use `/research` or `/brainstorm`
- One-off bug fixes — use `/debug`
- Tasks where the agent's "propose" step would be writing prose, not code (use `/dialectic-review --ideate` instead)

---

## Expected Frequency

Per one review pass: **sustained 3-6 month workhorse on whichever project has an active optimization shape**, not "weekly when shape appears." When a model-improvement phase is the active focus, autoresearch likely runs daily for weeks. Between active engagements, it sits idle.

Across the calendar: probably 2-3 sustained engagements per year (each spanning weeks), plus occasional one-week prompt-engineering sprints.

---

## Extensions (mode of thinking)

The core principle is **bounded autonomous iteration with revertability**. Human provides goal + budget + fitness function; agent operates within constraints until budget exhausts or fitness saturates. Two-track iteration (human owns prompt.md, agent owns script.py) keeps separation of concerns clean; branch commits keep every step reversible.

Extensions worth elaborating:

### 1. Meta-autoresearch on the workflow layer

Once `~/.claude/tools/skill-trigger-evals.py` exists, autoresearch can iterate on CLAUDE.md trigger phrasing against the trigger-eval JSONL — measuring trigger pass rate as the metric. **The workflow itself becomes optimizable.** This is the highest-leverage second-order application.

### 2. Experiment registry as cross-project corpus

Each project accumulates an `experiments.jsonl`. Across projects, this becomes a meta-corpus: **which prompt shapes moved metrics most in which domains?** A periodic cross-project query produces queryable artifacts under selection pressure — prompts that survived multiple wins propagate.

Eventually: `~/.claude/tools/autoresearch-meta.py` queries all `experiments.jsonl` files across projects and surfaces patterns ("LLM-as-judge prompts that include explicit rubric examples outperform open-ended ones by N points across 12 experiments").

### 3. Shape budget alongside wall-clock

Wall-clock budget explores breadth (many micro-tweaks). Shape budget enforces depth ("try ≥3 structurally different approaches before declaring done"). Pair them. Wall-clock alone produces local optima; shape budget forces exploration of qualitatively distinct strategies before committing.

The propose step should track "approaches tried" alongside iteration count, and refuse to converge until shape budget is satisfied even if wall-clock budget would allow another local-optima micro-step.

### 4. /dialectic-review as autoresearch on argument-strength

Numeric eval = referee's judgment scored against a committed rubric; variants = For/Against framings; loop = generate more variants, keep the strongest. Same mechanic applied to argumentation. Could be a `/dialectic-review --autoresearch` mode that runs many dialectic-review iterations against the same question, keeping only the strongest synthesis.

### 5. Eval-as-first-class-artifact

Per CLAUDE.md "Evals before specs" + this skill's hard requirement of `--metric`: the eval function is the most load-bearing artifact in any optimization project. It deserves its own version control history, its own tests, its own /review pass. Treat the eval as a first-class deliverable, not an afterthought.

Consider: every project that uses autoresearch should commit its eval function to `eval.py` in the project root with a Git history. The eval becomes the project's *constitution* — what it's optimizing for, made explicit.

---

## Anti-Patterns

- **"Improve this code" without a metric.** Refuse. This is the diagnostic test of whether autoresearch is being used correctly. Without a metric, the agent is narrating, not iterating.
- **LLM-as-judge with a non-fixed prompt.** Either commit the judge prompt + rubric + temperature=0, or use a different metric. Free-form "is this output better?" is vibes, not measurement.
- **No git branch.** Without revertability, you'll get stuck in a local optimum and have no way to recover.
- **Running on uncommitted code.** Baseline measurement is meaningless if the starting state isn't recorded.
- **Letting the loop run past usefulness.** If the last 5 iterations have all reverted or produced near-zero deltas, the metric has saturated for this approach. Exit; reconsider the prompt; restart with a new approach. The shape budget helps catch this automatically.

---

## Sources

- Andrej Karpathy (autoresearch pattern, raw/ + compiled wiki framing) — multiple tweets
- @altryne — Shopify Liquid templating engine, +53% via overnight autoresearch
- @witcheer — launchd + tmux + claude -p, 45 experiments/night
- @aakashgupta — Karpathy 630-line script, 100+ overnight ML experiments
- @archiexzzz — wall-clock + vocab-invariant metric
- @garybasin — hand-compute precursor; state-machine emulation
- Workflow dialectic review — selected as single highest-leverage addition
