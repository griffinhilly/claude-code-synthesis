# MCP Server Debugging on Windows — Encoding Gotcha

When an MCP server fails to start, appears connected but inert, or fails silently after token/config changes (a messaging-bot plugin, a chat-server integration, any bun-based MCP), **check the `.env` file encoding first**.

PowerShell and Notepad default to UTF-16 on Windows. Bun (and most MCP server runtimes) expect UTF-8. A UTF-16 `.env` causes the server to fail without surfacing a useful error — a plugin-reload command reports the server as configured, but it's inert.

**Why:** An MCP plugin's `.env` was written as UTF-16 by a prior PowerShell session. The MCP server failed silently on plugin reload. From the user-facing side it looked like the integration wasn't responding, not like a config error.

**How to apply:** When an MCP server appears configured but doesn't actually function (no responses, silent failures, connected-but-inert), check `.env` encoding before assuming the config is wrong:

```bash
file .env  # should say "ASCII text" or "UTF-8 Unicode text", NOT "Little-endian UTF-16"
```

If wrong, rewrite as UTF-8 via Python (Notepad's "Save As" UTF-8 option also works but writes a BOM that some runtimes reject; Python is cleaner).

## Python MCP Servers on Windows — Two More Gotchas

**1. Heavy C-extension imports deadlock in worker threads.** A FastMCP tool that lazily imports scipy/sklearn/torch (e.g. via sentence_transformers) hangs forever: the C-extension DLL load wedges inside the anyio worker thread while the main thread runs the event loop. Symptom: server responds to initialize/tools-list, then the first heavy tool call never returns; process becomes an unkillable zombie (loader lock) until reboot. **Fix: import + load heavy libraries on the MAIN thread before `mcp.run()`.** Diagnose with `faulthandler.dump_traceback_later(45, file=sys.stderr)` armed before `mcp.run()` — the stack dump shows exactly where threads are stuck (this beat two rounds of plausible-but-wrong hypotheses).

**2. stdout is the protocol channel.** Anything a library prints to stdout (HF "Loading weights" bars, transformers LOAD REPORT) corrupts JSON-RPC. Belt-and-braces: set `HF_HUB_DISABLE_PROGRESS_BARS=1`, `TQDM_DISABLE=1`, `TRANSFORMERS_VERBOSITY=error` before imports, AND wrap loads in `contextlib.redirect_stdout(sys.stderr)`. Test over real stdio (spawn the server, speak JSON-RPC) — build a small standalone test harness script that does this rather than trusting the harness's own client.
