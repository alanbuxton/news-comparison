# CLAUDE.md — Notes for Claude Code

## Running commands

Always use `uv run python` — never `python` directly or `pip`.

```sh
uv run python main.py 2026-03-08          # run benchmark, saves to results/2026-03-08/
uv run python analyse.py results/2026-03-08   # run AI analysis on those results
uv run python analyse.py results/2026-03-02   # re-analyse an older run
```

Installing packages:

```sh
uv add <package>       # add dependency
uv add --dev <package> # add dev dependency
```

## Project structure

| File | Purpose |
|---|---|
| `main.py` | Runs all providers, writes companies.csv + industries.csv |
| `analyse.py` | Calls Claude API with anonymised data, writes analysis markdown |
| `examples.py` | Company names and industry/location combos used in queries |
| `utils.py` | Shared config: API key loading, 90-day date window, error logging |
| `exa_client.py` | Exa provider wrapper |
| `linkup_client.py` | Linkup provider wrapper |
| `perplexity_client.py` | Perplexity provider wrapper |
| `syracuse_client.py` | Syracuse provider wrapper |
| `tavily_client.py` | Tavily provider wrapper |
| `newsapi_client.py` | NewsAPI wrapper (currently excluded from CLIENTS in main.py) |

Results go to `results/{prefix}/` (companies.csv, industries.csv, errors/, AI-analysis/).

## Key design decisions

**Why provider names are anonymised in analyse.py:** The author of this repo is also the author of Syracuse. Any AI model that knows this may unconsciously soften criticism of Syracuse. The anonymisation (random shuffle to letters A–E) ensures the model evaluates on data alone. The decode key is saved locally. Do not remove this feature.

**Why MAX_ARTICLES_PER_QUERY = 15:** This caps the number of articles shown per company/topic per provider to keep the prompt within Claude's context window while still giving enough data to spot patterns (false positives, duplicate articles, missing dates). Increase if the model misses patterns; decrease if costs are a concern.

**Why the system prompt forbids hedging:** The point of this tool is to get honest competitive intelligence about where Syracuse falls short. A model that hedges or refuses to rank defeats the purpose.

## The article schema

Both CSVs share the same columns:

| Column | Notes |
|---|---|
| `company` | Populated for company queries |
| `industry` | Populated for industry queries |
| `location` | Populated for industry queries |
| `provider` | One of: Exa, Linkup, Perplexity, Syracuse, Tavily |
| `headline` | Article title; `*** ERROR ***` for failed calls |
| `published_by` | Publisher / news source name |
| `published_date` | Raw date string from provider |
| `published_date_clean` | Parsed datetime with timezone |
| `activity_type` | Optional classification from provider (e.g. M&A, Earnings) |
| `document_url` | URL of the article |
| `summary_text` | Provider-supplied summary or scraped text |

Error rows have `headline = "*** ERROR ***"` and are counted separately in the analysis — they are a signal of provider reliability.

## Adding a new provider

1. Create `{name}_client.py` implementing `get_company_articles_for(company: str)` and `get_industry_articles_for(industry: str, location: str)`. Each returns a list of article dicts matching the schema above.
2. Add it to the `CLIENTS` dict in `main.py`.
3. No changes needed to `analyse.py` — it discovers providers from the CSV data.

## Environment variables

All in `.env` (loaded via python-dotenv):

```
EXA_API_KEY
LINKUP_API_KEY
PERPLEXITY_API_KEY
SYRACUSE_API_KEY
TAVILY_API_KEY
NEWSAPI_API_KEY
ANTHROPIC_API_KEY     # required for analyse.py
```
