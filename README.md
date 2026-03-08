# AI News Provider Comparison

Benchmarking news search providers against each other on the same queries, then using an AI judge to score the results.

Providers currently in the comparison:

- [Exa](https://exa.ai)
- [Linkup](https://linkup.so)
- [Perplexity](https://perplexity.ai)
- [Syracuse](https://syracuse.1145.am) *(author's project)*
- [Tavily](https://tavily.com)

## How it works

Two types of query are benchmarked:

- **Company queries** — news about specific named companies (e.g. ExxonMobil, Commerzbank, Klöckner Pentaplast). The mix deliberately includes large well-known companies, mid-tier companies, and small/obscure companies with low digital footprint.
- **Industry/location queries** — news about an industry sector in a geography (e.g. PE Resins in the US, Road Freight in Europe).

For each query, every provider is called with the same parameters and its results are written to a shared CSV. An AI judge then scores the results.

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
| `PERPLEXITY_API_KEY` | Perplexity |
| `SYRACUSE_API_KEY` | Syracuse |
| `TAVILY_API_KEY` | Tavily |
| `ANTHROPIC_API_KEY` | Claude (for analysis step) |

### 2. Run the comparison

```sh
uv run python main.py 2026-03-08
```

This writes results to `results/2026-03-08/`:

```
results/2026-03-08/
  companies.csv     # all provider results for company queries
  industries.csv    # all provider results for industry/location queries
  errors/           # per-provider error logs
```

### 3. Run the AI analysis

```sh
uv run python analyse.py results/2026-03-08
```

This writes to `results/2026-03-08/AI-analysis/`:

```
  claude-companies-{timestamp}.md    # scored analysis for company queries
  claude-industries-{timestamp}.md   # scored analysis for industry queries
  decode-key-{timestamp}.json        # maps A/B/C/D/E back to real provider names
```

You can also analyse a previous run:

```sh
uv run python analyse.py results/2026-03-02
```

And use a cheaper model for quick iteration:

```sh
uv run python analyse.py results/2026-03-08 --model claude-sonnet-4-6
```

## Anti-bias design

The author of this benchmark is also the author of Syracuse. This creates an obvious risk: any AI with knowledge of Syracuse — and knowledge that it is being evaluated by its author — might soften its criticism or give it undeserved benefit of the doubt.

`analyse.py` addresses this with three measures:

**1. Provider name anonymisation.** Before any data is sent to the AI, the five provider names are randomly shuffled and replaced with letters (A, B, C, D, E). The mapping is stored locally in `decode-key-{timestamp}.json` but the AI never sees it. The AI cannot defer to "Syracuse" because it does not know which label it is.

**2. Unsparing system prompt.** The model is explicitly instructed that hedging is forbidden, that every negative claim must be backed by a specific article example, and that it must produce a strict rank order — not a "different providers suit different needs" conclusion. The instruction to describe what each lower-ranked provider would need to fix to reach first place forces the model to articulate concrete gaps rather than glossing over them.

**3. Consistent evaluation criteria.** The prompt specifies the same criteria for every provider: precision (false positive rate), coverage of obscure entities, date accuracy, summary usability (can you understand the story without clicking?), source quality, paywall accessibility, and hallucination risk.

## Interpreting the output

The analysis files use Provider A/B/C/D/E throughout. To decode:

1. Open the `decode-key-{timestamp}.json` file alongside the analysis:
   ```json
   { "label_to_provider": { "A": "Exa", "B": "Syracuse", ... } }
   ```

2. The analysis will have ranked providers 1st–5th and listed specific improvements needed for each. Cross-reference with the decode key to identify which provider is which.

3. Pay particular attention to the **"What each provider needs to fix"** section — this is where the most actionable competitive intelligence lives.

Note: the mapping is re-randomised on every run of `analyse.py`, so Provider A in one run is not necessarily the same as Provider A in another.

## What is evaluated

| Criterion | What counts as failure |
|---|---|
| Precision | Article is about a completely different company/industry that merely shares a name fragment (false positive) |
| Significance | Company/industry is mentioned but nothing useful is communicated — trivial name-drops in unrelated roundups |
| Coverage | No results at all for obscure or small companies |
| Date accuracy | Dates missing, or article assigned a date that differs from its actual publication date |
| Summary usability | Raw scraped boilerplate (nav menus, cookie banners) instead of a distilled summary |
| Source quality | Aggregators that add no value, product pages, "About Us" content, market research landing pages. Press releases are fine. |
| Paywall | Source is subscriber-only with no usable preview |
| Hallucination | URLs that do not correspond to real published articles; invented facts in summaries |

## Results history

### 2026-03-08

Syracuse ranked 1st in both query types:

- **Companies:** Syracuse 1st (highest precision, zero hallucination), Linkup 2nd (best summaries, entity disambiguation gaps), Perplexity 3rd (hallucination risk on obscure companies), Tavily 4th (no dates on any article), Exa last (broken relevance — same irrelevant articles returned for every company).
- **Industries:** Syracuse 1st (precise, clean dates, no hallucination), Exa 2nd (covers all topics but 20% errors and syndication spam), Tavily 3rd (zero dates, topic mismatches), Perplexity 4th (ranked down from surface quality due to systematic hallucination), Linkup last (90.7% error rate — effectively non-functional). [Details](results/2026-03-08/AI-analysis/claude-companies-20260308-231709.md)

### 2026-03-02

No single winner across both query types:

- **Industries/Regions:** Syracuse favoured, Exa second.
- **Companies:** Perplexity/Linkup (ChatGPT) or Syracuse/Linkup (Claude).
- Tavily last in both. [Details](results/2026-03-02/README.md)

### 2026-02-10

Added Exa and Tavily. Syracuse remains preferred overall. [Details](results/2026-02-10/README.md)

### 2026-02-01

ChatGPT, Grok, Claude, and Gemini all prefer Syracuse. Copilot prefers Linkup. [Details](results/2026-02-01/README.md)

### 2026-01-06

Perplexity appeared to have improved but was found to be surfacing old articles with new dates — high false-positive rate. Syracuse holds up well for industry news. AI analysis results varied across models and accounts. [Details](results/2026-01-06/README.md)

### 2025-08-30

After changes to Syracuse, now a stronger contender for company-specific news. [Details](results/2025-08-30/README.md)

### 2025-05-27

None of the three original providers (Perplexity, Linkup, Syracuse) reliably handles industry/region queries. Linkup best for company news at this point. [Details](results/2025-05-27/README.md)
