# How the benchmark works

Details behind the [results summary in the README](README.md#results-history).

## Running the benchmark

### 1. Setup

Copy `.env.sample` to `.env` and fill in your API keys:

```sh
cp .env.sample .env
```

Keys needed:

| Variable | Provider |
|---|---|
| `EXA_API_KEY` | Exa |
| `LINKUP_API_KEY` | Linkup |
| `PERPLEXITY_API_KEY` | Perplexity (both Search and Agent) |
| `SYRACUSE_API_KEY` | Syracuse |
| `TAVILY_API_KEY` | Tavily |
| `NEWSAPI_API_KEY` | NewsAPI (client exists but is not run) |
| `ANTHROPIC_API_KEY` | Claude (for the analysis step) |

Which providers run is set by the `CLIENTS` dict in `main.py`. Comment a
provider out to drop it from a run. Tavily has been left out of runs since
2026-09-06.

### 2. Run the comparison

```sh
uv run python main.py 2026-03-08
```

Each provider is asked for news from the last 90 days, at most 20 results per
query. Results are written to `results/2026-03-08/`:

```
results/2026-03-08/
  companies.csv     # all provider results for company queries
  industries.csv    # all provider results for industry/location queries
  errors/           # per-provider error logs
```

Failed calls appear in the CSVs as rows with headline `*** ERROR ***`. They
are counted against the provider's reliability.

### 3. Run the AI analysis

```sh
uv run python analyse.py results/2026-03-08
```

This writes to `results/2026-03-08/AI-analysis/`:

```
claude-companies-{timestamp}.md     # scored analysis for company queries
claude-companies-{timestamp}.json   # machine-readable scorecard
claude-industries-{timestamp}.md    # scored analysis for industry queries
claude-industries-{timestamp}.json
decode-key-{timestamp}.json         # maps the anonymised letters back to provider names
```

It also prints a summary for the README's results history.

Other options:

```sh
uv run python analyse.py results/2026-03-02                          # re-analyse an older run
uv run python analyse.py results/2026-03-08 --model claude-sonnet-4-6 # cheaper model for quick iteration
uv run python analyse.py results/2026-03-08 --max-articles 15        # show the judge fewer articles per item
uv run python analyse.py results/2026-03-08 --readme-only            # regenerate the README summary from existing analysis files
```

The default judge model is `claude-opus-4-7`. The judge is shown up to 20
articles per company or topic per provider.

## Anti-bias design

The author of this benchmark is also the author of Syracuse. This creates an obvious risk: any AI with knowledge of Syracuse — and knowledge that it is being evaluated by its author — might soften its criticism or give it undeserved benefit of the doubt.

`analyse.py` addresses this with four measures:

**1. Provider name anonymisation.** Before any data is sent to the AI, the provider names are randomly shuffled and replaced with letters (A, B, C…, one per provider in the run). The mapping is stored locally in `decode-key-{timestamp}.json` but the AI never sees it. The AI cannot defer to "Syracuse" because it does not know which label it is.

**2. Unsparing system prompt.** The model must use the full 0–10 range, may not give everyone the same middling score, and must back every score with concrete evidence that names a queried company or topic and quotes a headline, source or count.

**3. Ground-truth flags computed by the harness.** Dates, duplicates, market-report pages, not-news pages, missing publishers and errors are detected in code, not left to the model's judgement (see [Flags](#flags-computed-by-the-harness)). Everything a provider returns — headline, summary, publisher, any label — is treated as that provider's claim, to be checked against the rest of the row.

**4. The harness does the arithmetic.** The model only scores each axis. The weighted score, the caps and the final ranking are computed in code, so the model cannot quietly reorder providers.

## What is evaluated

Each provider is scored 0–10 on five axes, separately for company queries and industry queries:

| Axis | Weight | 10 looks like | 0 looks like |
|---|---|---|---|
| Precision | 35% | Every returned article is relevant and on-topic | Wrong-entity, off-topic, not-news or stale content; or no results at all |
| Coverage | 20% | At least one real, relevant article for nearly every queried company or topic | Many queried companies or topics get no results |
| Metadata integrity | 15% | Every article has a date within the 90-day window and a named publisher | Many articles with no date or a stale date (severe); many with no publisher (about half as severe) |
| Story quality | 15% | Summaries let the user decide without clicking | Boilerplate, cookie banners, "subscribe to read" |
| Trust | 15% | No errors, no suspicious URLs | Hallucinated URLs or facts; high error rate |

The scoring prefers avoiding false positives over finding every story: 5 clean on-topic articles beat 30 articles of which half are about the wrong company.

### Caps

Some failures cannot be made up for by strength elsewhere. The final score is capped when:

| Condition | Final score capped at |
|---|---|
| Metadata integrity ≤ 3 | 5.0 |
| Metadata integrity ≤ 5 | 7.0 |
| Trust ≤ 4 | 4.0 |
| Precision ≤ 3 | 5.0 |

Providers are ranked by final score. Ties are broken by precision, then metadata integrity.

### Flags computed by the harness

These are marked on each article before the judge sees it, and counted per provider:

| Flag | Meaning |
|---|---|
| No date | The provider gave no publication date |
| Stale | Dated more than 90 days before the run |
| No publisher | The provider gave no publisher name. The article's domain is shown instead, but a domain is not credited as a publisher because any URL yields one |
| Duplicate | Same headline as another article from that provider, whichever outlet carried it |
| Market report | A market-research landing page or SEO announcement, not news |
| Not news | Social posts, forum threads, videos and company About pages |
| No results | The provider returned nothing for that company or topic |

The judge also gets two harness-computed sections when they apply:

- **Provider self-reported relevance.** Where a provider returns its own relevance score (in practice only Tavily), the harness reports items where it returned many articles but scored all of them as weak. Nothing is filtered out on the score.
- **Spelling-variant consistency.** Some companies are queried under two spellings (e.g. "Klöckner Pentaplast" and "Klockner Pentaplast"). For each provider this shows the article count for each spelling and how many URLs the two have in common. Answering only one spelling counts as a missed company.

## Interpreting the output

The analysis files use the anonymised letters throughout. To decode:

1. Open the `decode-key-{timestamp}.json` file alongside the analysis:
   ```json
   { "label_to_provider": { "A": "Syracuse", "B": "Linkup", ... } }
   ```

2. In each analysis `.md`, the **Recomputed scorecard** table is authoritative: the axis scores are the model's, and the weighted score, caps, final score and rank are recomputed by the harness. If numbers in the model's raw output disagree with it, the table wins.

3. The evidence strings under each axis and the **Notes** section say what each provider got wrong, with examples. That is where the most actionable competitive intelligence lives.

Note: the mapping is re-randomised on every run of `analyse.py`, so Provider A in one run is not necessarily the same as Provider A in another.
