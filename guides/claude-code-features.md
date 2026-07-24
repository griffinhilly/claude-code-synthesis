# Claude Code Features (superseded)

This guide previously cataloged Claude Code's native feature set as of early 2026 (sourced from a Boris Cherny thread). That catalog went stale within months — named commands changed, features shipped and were renamed — which is itself the lesson: **don't maintain a hand-written mirror of a fast-moving product's feature list.**

Where to look instead:

- **Session-management primitives** (`/rewind`, `/clear`, `/compact` with steering, `!` shell prefix, keybindings): `claude-code-primitives.md` in this directory — scoped to the small set of moves our workflow actually depends on, with a "check for drift" caveat.
- **The current full feature set**: the official docs at https://docs.anthropic.com/en/docs/claude-code and `claude --help`, which are always current.
- **What this repo adds on top of native features**: `skills-reference.md` in this directory.

Rule of thumb encoded from this file's failure: when a guide's value depends on external product state, either scope it to the few load-bearing features you actually use (and date-stamp it), or point at the authoritative source — never mirror the whole surface.
