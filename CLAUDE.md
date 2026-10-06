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
| `utils.py` | Shared config: API key loading, 90-day date window, error logging, `publisher_domain` |
| `queries.py` | Canonical query text shared by all providers |
| `exa_client.py` | Exa provider wrapper |
| `linkup_client.py` | Linkup provider wrapper |
| `perplexity_search_client.py` | Perplexity Search API wrapper (`/search`) |
| `perplexity_agent_client.py` | Perplexity Agent API wrapper (`/v1/agent`) |
| `syracuse_client.py` | Syracuse provider wrapper |
| `tavily_client.py` | Tavily provider wrapper |
| `newsapi_client.py` | NewsAPI wrapper (currently excluded from CLIENTS in main.py) |

Results go to `results/{prefix}/` (companies.csv, industries.csv, errors/, AI-analysis/).

## Key design decisions

**Why provider names are anonymised in analyse.py:** The author of this repo is also the author of Syracuse. Any AI model that knows this may unconsciously soften criticism of Syracuse. The anonymisation (random shuffle to letters A, B, C… — one per provider, currently six) ensures the model evaluates on data alone. The decode key is saved locally. Do not remove this feature.

**Why there are two Perplexity clients:** Perplexity ships two APIs that behave
so differently they cannot fairly share one row in the comparison.
`perplexity_search_client.py` calls `/search`, which returns real indexed pages
— no model name, no publisher field, and a hard cap of 20 results per query.
`perplexity_agent_client.py` calls `/v1/agent`, which synthesises an article
list with publisher names and written summaries. Both are listed in `CLIENTS`;
comment either out for a given run. `make_anonymization` scales past five
providers automatically, and the prompt text takes its provider count and label
range from the run via `fill_provider_counts`, so running both is safe.

**Why the Agent client replaced the Sonar one:** Perplexity retires
`/chat/completions` on 2026-09-27, so benchmarking it is not useful to anyone
choosing a provider now. Sonar tiers map onto Agent presets (`sonar` → `fast`,
`sonar-pro` → `low`, `sonar-reasoning-pro` → `medium`, `sonar-deep-research` →
`high`); the client uses `low`, the old `sonar-pro` equivalent, set as `PRESET`.
The old client is recoverable with `git show 5380b36:perplexity_client.py`.

**Why the Agent client puts the date window in the prompt:** `/v1/agent` rejects
`search_after_date_filter` / `search_before_date_filter` with `unknown field`,
unlike both Sonar and the Search API. The window is therefore requested in the
prompt and genuinely enforced by `filter_recent_real_articles` in `main.py`.

**Why the Agent client ignores the `search_results` blocks:** the response
carries the raw retrieved pages alongside the synthesised answer, and it would
be easy to cross-check returned URLs against them. Doing so would hide
fabricated URLs — a defect this benchmark exists to detect, and Sonar's historic
failure mode (see the 2026-05-11 and 2026-03-31 runs). The synthesis path is
read as-is, on purpose. Reading the raw pages instead would also just duplicate
what `perplexity_search_client.py` already measures.

**Why `examples.py` queries some names twice:** "Klöckner Pentaplast" and
"Klockner Pentaplast" are one company under two spellings. `analyse.py` folds
queried names on accent/case/punctuation (`_variant_key`), and where two names
collapse to the same key it emits a `SPELLING-VARIANT CONSISTENCY` section:
per provider, the article count for each spelling and the share of returned
URLs common to both. Previously the judge saw the two as unrelated companies
and the robustness question — does the provider still find the company when
the caller omits the umlaut? — never reached the report. The section is
harness-computed ground truth, feeds `coverage` (answering one spelling only is
a missed entity) and `precision` (junk under one spelling), and is also written
into the saved `.md` and the JSON scorecard as `spelling_variants`, so the
finding lands whether or not the model cites it. Pairs are detected from names
present in the CSV, never from the current `examples.py` — re-analysing an old
run must not be reinterpreted through today's query list.

**Why some `examples.py` rows are commented out:** rows tagged `# CUT:` put
every provider in the same bucket across the 2026-05-28, 2026-07-05 and
2026-08-09 runs (all junk, all good, or a duplicate of another row), so they
burned API calls and prompt budget without separating anyone. Cut on
2026-08-19. Worth re-testing occasionally — a provider improving could make one
discriminating again.

**Why Tavily's dates changed in 2026-08:** `tavily_client.py` requested
`topic="news"` — which per Tavily's docs "includes `published_date` metadata" —
but `item_to_article` hardcoded `published_date` to `""`, so every Tavily row
landed dateless. That is the origin of the "100% no-date" verdicts in every run
up to and including 2026-08-09 (4,406 undated articles in 2026-07-05 alone) and
the recency caps those triggered. It was a bug in this repo, not a Tavily
defect. Results from before this fix understate Tavily and are not comparable
with later runs on the date axis.

**Why `published_by` and `publisher_domain` are separate:** only some APIs
return a publisher name (Linkup, Syracuse, Perplexity Agent). Exa, Tavily and
Perplexity Search return none. Exa's client used to synthesise one from
`netloc` plus `item.author`, which made it look better than Perplexity Search on
identical underlying data — and `item.author` is unreliable anyway, sometimes a
journalist and sometimes a publication. Now `published_by` holds only what the
provider actually gave, and `publisher_domain` is derived from the URL centrally
in `main.py` so every provider gets it identically. Scoring runs on
`published_by`; the domain is shown to the judge alongside, which is why a
missing publisher is weighted at roughly half the severity of a missing date
rather than equally. Do not credit the domain as a publisher — it is derivable
from any URL, so it would score every provider the same and measure nothing.
`classify_publisher` sets the flag, the provider header carries a
`no-publisher: N (X%)` count, and the axis that scores it was renamed from
`recency_integrity` to `metadata_integrity` when publishers joined dates on it.

**Why duplicate detection keys on the headline stem alone:** it used to key on
`(published_by, headline_stem)`. Once `published_by` became genuinely blank for
three providers, that key collapsed unrelated stories together for them while
letting providers that do return a name escape cross-outlet syndication
detection. A matching 60-char stem is the same story whoever carried it, and the
stem is available for every provider.

**Why query wording lives in `queries.py`:** the per-client prompts had drifted.
Some providers were told to prefer "credible business, trade, specialized or
regional news sources" and others were not, which quietly advantaged the ones
that got the steer. The substance is defined once now, in two forms — `keyword`
for retrieval engines (Exa, Tavily, Perplexity Search) and `prose` for
LLM-driven ones (Linkup, Perplexity Agent). Clients append only output-format
wording, which is an API constraint rather than part of the question. Syracuse
takes structured parameters and uses none of it.

**Why company and industry topic lists are separate:** normalising both onto one
company-shaped list ("financial performance", "supplier risk") made Linkup
return 0 articles for `BOPET | CN`, a topic that returns ~10 under the industry
list — verified by bisecting the query. Company news and industry news are
different questions; what is normalised is that every provider gets the *same*
list for a given query type, not that both query types share one list.
`test_clients.py` pins the two apart.

**Why Linkup runs at `depth="deep"`:** it was on `"standard"` while Tavily ran
at `search_depth="advanced"`, so Linkup was being benchmarked on its basic tier
against Tavily's premium one. Linkup's high error rates in earlier runs may
partly reflect that.

**Why Syracuse gets no date window:** its API supports only "last 7 / 30 / 90
days" rather than explicit bounds, so the 90-day window is left to
`filter_recent_real_articles` in `main.py`.

**Why Syracuse summaries can open with a `[Name: role]` note:** every other
provider's summary is chosen for the query — an LLM-written summary (Perplexity
Agent, Linkup) or the passage the engine matched (Exa highlights, Perplexity
Search snippets). Syracuse's `document_extract` is the article's lead whatever
the query, so on a funding round it never reaches the investor list, and the
judge read Bloomberg Beta's investments as name-drops (2026-09-27 run). The
Syracuse API names the searched company and its role in each row
(`matched_organizations`, part of its default simple output since 2026-10),
and `syracuse_client.py` puts it at the head of `summary_text`, the field every
provider fills. It is mapped from what the API returns to any caller, never
built in p-v-s. A confident label could make a wrong-entity row look relevant,
but so could an LLM summary that invents facts, so the judge rule is general
and names no format: only the harness's flags are ground truth, and every
provider field — headline, summary, publisher, any label — is that provider's
claim, judged by what the whole row supports. Runs before and after this change
are not comparable on Syracuse company precision.

**Why Exa and Tavily are capped at 20 results:** `num_results` / `max_results`
is the caller's request, not a measure of the provider, and asking Exa for 50
and Tavily for 100 while others are structurally limited to provide only 
relevant results without padding with lower-value results didn't make for a fair
like-for-like comparison. It also interacted badly with `DEFAULT_MAX_ARTICLES`:
every client sorts by date, so the 15 articles the judge sees were the 15 most
*recent* of the 50, which for a relevance-ranked list is close to a random
sample. Measured on 12 companies, that put Exa's shown articles at 34%
on-target; asking for 20 instead raises it to 47% and asking for 10 to 61%,
while the number of genuinely on-target articles reaching the judge goes *up*.
20 is the settled figure because it keeps Exa above the 15-article display cap
so it is not handicapped on `coverage`. Exa's own ranking is worth respecting —
70% on-target at ranks 1-5 decaying to 23% at 41-50 — and at 50 you also pay
Exa for every result past the tenth.

**Why `relevance_score` is recorded but never filtered on:** Tavily returns a
real relevance score and sorts by it, and it separates cleanly — in a
12-company probe, none of the 414 results scoring below 0.1 were on-target,
against ~72% above 0.3. Dropping those rows would raise Tavily's measured
precision from 8% to 72%, which is exactly why the harness must not do it:
returning 79 articles for "Klöckner Pentaplast" whose best score was 0.115 is a
precision failure, and filtering it out would perform the quality work the
provider declined to do and then hide that it was needed. Same reasoning as the
Perplexity Agent client ignoring `search_results`. The score is instead reported
as ground truth by `score_diagnostics` / `score_block` / `score_table_md`, which
flag items a provider answered while scoring *every* returned article below
`WEAK_SCORE` (0.2, empirically derived from Tavily and not calibrated across
providers). Exa is the other half of the finding: it returns no score under
`type="auto"` and, under `type="neural"`, `1 - i/(n-1)` — a rank ramp identical
for a company with 45 good hits and one with none. That absence is reported as a
usability limitation, not scored as a precision failure.

**Why `DEFAULT_MAX_ARTICLES` = 20:** every provider returns at most 20 per
query, so 20 shows the judge everything. It was 15 from the first version
(2026-03-08), set for context-window headroom and never tuned. At 15 the cap hid
rows only from the high-volume providers — Exa and Perplexity Search on every
item, Syracuse on some — and rows 16–20 are where wrong-entity padding sits, so
their precision was judged on their best rows while the low-volume providers
were judged on everything. Going to 20 costs roughly a quarter more input
tokens per judge call (estimated ~230k → ~290k for companies on the 2026-09-27
data). Lower it only if a prompt stops fitting, and then prefer sampling across
the list to truncating its tail.

**Why there is a `[NOT-NEWS ⚠]` flag:** the rubric always counted social posts,
forum threads, videos and About pages as FP-not-news, but nothing detected them,
so whether they cost precision depended on the judge noticing a domain. The
harness now flags them like market reports (`_is_not_news`: social/forum/video
domains, plus About-page path segments unless a newsroom segment such as
`/news-and-deals/` or `/press-room/` is present — those are press releases),
counts them over every row, and the prompt makes each flagged row an FP. On the
2026-09-27 data it flags 135 Perplexity Search and 14 Exa rows (almost all
LinkedIn posts and Pulse articles) and none from the other providers. The flag
is a floor: catalogues, registry listings and blogs still rely on the judge.

**Why the system prompt forbids hedging:** The point of this tool is to get honest competitive intelligence about where Syracuse falls short. A model that hedges or refuses to rank defeats the purpose.

## The article schema

Both CSVs share the same columns:

| Column | Notes |
|---|---|
| `company` | Populated for company queries |
| `industry` | Populated for industry queries |
| `location` | Populated for industry queries |
| `provider` | One of: Exa, Linkup, Perplexity Search, Perplexity Agent, Syracuse, Tavily |
| `headline` | Article title; `*** ERROR ***` for failed calls |
| `published_by` | Publisher name **as supplied by the provider**; blank if its API returns none |
| `publisher_domain` | Hostname of `document_url`, derived centrally in `main.py` for every provider |
| `published_date` | Raw date string from provider |
| `published_date_clean` | Parsed datetime with timezone |
| `activity_type` | Optional classification from provider (e.g. M&A, Earnings) |
| `document_url` | URL of the article |
| `summary_text` | Provider-supplied summary or scraped text |
| `relevance_score` | Provider's own relevance score; blank where it supplies none (only Tavily's is meaningful). Reported, never used to filter |

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
