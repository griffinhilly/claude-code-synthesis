# PostgreSQL Query Batching

When doing exploratory database work that requires repeated human approval for each query, batch queries to reduce friction.

## Strategies

1. **Batch read-only queries** into a single Python script that runs multiple SELECTs and prints all results at once — one approval instead of ten
2. **Use CTEs** to chain dependent queries into a single statement
3. **Ask about `--dangerously-skip-permissions`** for read-only exploration sessions — the user may prefer to grant blanket read access rather than approving every SELECT

## Reminders

- Use Python (psycopg2/sqlalchemy) for DB access rather than raw psql CLI — it's more portable and scriptable
- Never run INSERT/UPDATE/DELETE/DROP without explicit confirmation, even in batch mode
