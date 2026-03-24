# Agent Orchestration Reference

## Batch LLM Categorization with Claude Code

The categorization step uses Claude Code sub-agents to process records in batches. This is the most powerful pattern in the pipeline — it lets you run LLM classification over thousands of records cheaply and quickly.

### Recommended Setup

- **Model**: Claude Haiku (fast, cheap, good enough for classification)
- **Batch size**: 20-25 records per agent
- **Parallelism**: Run multiple agents concurrently via Claude Code's Agent tool
- **Output format**: JSON keyed by record ID (matches the merge utility's expected input)

### How It Works

1. **Prepare the prompt** using `shared/taxonomy.py`:
   ```python
   from shared.taxonomy import get_system_prompt
   prompt = get_system_prompt()
   ```

2. **Format a batch** of records as context for the agent:
   ```
   Here are records to categorize:

   ID: record_123
   Text: "The product exceeded my expectations..."

   ID: record_456
   Text: "Battery life is terrible compared to..."
   ```

3. **Run the agent** with Claude Code's Agent tool, passing the system prompt + batch

4. **Parse the JSON output** and merge into `categories.json`

### Tips

- **20-25 per batch is the sweet spot.** Too few = overhead per agent. Too many = context length issues and quality degradation.
- **Always include the full taxonomy in the prompt.** Don't assume the model remembers from previous calls.
- **Expect invalid tags.** LLMs will hallucinate variations ("tech" instead of "electronics"). The fix maps in `taxonomy.py` handle this — that's why the verify step exists.
- **Check coverage after each batch run.** The pipeline's step 4 tells you how many records still need categorization.
- **Save intermediate results.** Write each batch's output to `categories.json` incrementally so you don't lose progress if something fails.

### Practical Example

In Claude Code, you might orchestrate like this:

```
You: Categorize these 25 records using the taxonomy in shared/taxonomy.py.
     Output JSON keyed by item_id.
     [paste records here]

Claude: [runs Agent tool with Haiku model, returns JSON]

You: [merge output into categories.json]
     python verify_and_merge.py   # validate and merge
```

### Quality Checks

After batch categorization, `verify_and_merge.py` gives you:
- **Coverage**: what percentage of records are categorized
- **Fix count**: how many invalid tags were auto-corrected
- **Distribution summary**: topic and content type counts for spot-checking

If a topic is suspiciously over- or under-represented, re-examine a sample from that batch.

### Cost Estimate

With Haiku at ~$0.25/MTok input + $1.25/MTok output:
- 1,000 records × ~200 tokens each = ~200K input tokens per batch run
- Total cost for 1,000 records: roughly $0.10-0.30

This makes it practical to iterate on your taxonomy and re-categorize if needed.
