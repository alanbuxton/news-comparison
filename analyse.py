#!/usr/bin/env python3
"""
Automated analysis of provider comparison results using the Claude API.

Provider names are randomly anonymised before the AI sees any data.
This prevents the model from adjusting its assessment based on knowing
which provider belongs to the user. The decode key is saved alongside
the analysis so results can be interpreted afterwards.

Usage:
    python analyse.py results/2026-03-02
    python analyse.py results/2026-03-02 --output-dir results/2026-03-02
    python analyse.py results/2026-03-02 --model claude-opus-4-6
    python analyse.py results/2026-03-02 --max-articles 20
"""

import argparse
import csv
import json
import os
import random
import string
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone

import anthropic
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-opus-4-6"
DEFAULT_MAX_ARTICLES = 15   # per company/topic per provider
MAX_SUMMARY_CHARS = 200     # truncate summaries to keep prompt manageable
STALE_DAYS = 90             # articles older than this are flagged as stale


def _parse_clean_date(raw: str) -> datetime | None:
    raw = (raw or "").strip()
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def classify_date(art: dict, reference: datetime) -> str:
    """Return "no_date", "stale", or "recent" for an article."""
    dt = _parse_clean_date(art.get("published_date_clean", ""))
    if dt is None:
        return "no_date"
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    age = reference - dt
    if age > timedelta(days=STALE_DAYS):
        return "stale"
    return "recent"


def reference_date_from_results_dir(results_dir: str) -> datetime:
    """Use the results folder name (e.g. 2026-04-20) as the reference date;
    fall back to now. Anchoring to the run date means re-analysing old folders
    doesn't falsely flag everything as stale."""
    name = os.path.basename(os.path.normpath(results_dir))
    try:
        return datetime.strptime(name, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    except ValueError:
        return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a ruthlessly objective product quality analyst. Your only job is to tell
the truth about what the data shows, clearly and without softening.

Non-negotiable rules:
1. No hedging. If a provider's output is bad, say it is bad. If it is mediocre,
   say it is mediocre. Qualifiers like "while it has room for improvement" are
   forbidden when the data clearly shows failure.
2. Every claim must be backed by a specific example from the data — name the
   company or topic and the article headline. General statements without evidence
   are not acceptable.
3. You must produce a strict rank order, 1st through 5th. Do not conclude that
   "different providers suit different needs" as a way to avoid ranking. One is
   best overall and one is worst overall — identify them.
4. For every provider not ranked 1st, state specifically what it would need to
   fix to become the best. "Better quality" is not acceptable — name the concrete
   change (e.g., "eliminate hallucinated URLs", "add date extraction", "fix
   entity disambiguation so 'Sigma Lithium' is not returned for 'Sigma Chemtrade'").
5. You do not know who built any of these providers. Treat Provider A, B, C, D,
   and E as completely interchangeable labels. Your score must be based solely on
   the data.
6. Even the top-ranked provider has flaws. List them.
"""

COMPANIES_PROMPT = """\
Five news search providers (labelled A–E, real names hidden) were each asked to
return news articles about specific companies over the past 3 months.

USER CONTEXT
The user is a business professional preparing for meetings. They need strategic
developments: M&A, financial results, product launches, regulatory issues,
executive changes, market expansion. They do not want noise.

WHAT COUNTS AS GOOD
- Real article or press release containing substantive information about the
  company (M&A, financials, product launches, regulatory matters, executive
  moves, expansion)
- The company is mentioned significantly — it does not have to be the sole
  subject, but the mention must be informative, not just a name-drop
- Date is present and within the last 90 days (the query window)
- Summary is informative enough to understand the story without clicking through
- URL is accessible without a paywall
- No hallucinated content (fabricated URLs, invented facts)

WHAT COUNTS AS BAD
- Articles about a completely different company that merely shares part of a name
  (e.g., returning "Sigma Lithium" results for a search on "Sigma Chemtrade" —
  this is a false positive and wastes the user's time)
- Trivial or insignificant mentions: the company name appears but nothing useful
  is communicated about it (e.g., a macro market roundup that lists the company
  alongside fifty others with no specific information)
- "About Us" pages, product catalogues, consumer how-to guides — not news
- **Missing dates** — flagged inline as `[NO DATE ⚠]`. Serious failure: the user
  cannot judge whether the news is current.
- **Stale dates** — flagged inline as `STALE>90d ⚠`. The query window is the
  last 90 days; anything older is off-scope by construction and equivalent to
  a wrong-topic result.
- Raw scraped page boilerplate as a "summary" (navigation menus, cookie banners,
  subscription prompts)
- No coverage of obscure or small companies
- Hallucinated articles (URLs that follow suspiciously neat patterns or
  do not correspond to real published content)
- Paywalled articles with no usable content

Each provider block's header lists exact counts: `no-date: N | stale (>90d): N`.
Use those numbers — do not estimate.

---

{data}

---

Provide your analysis in this exact structure:

## 1. Provider-by-Provider Assessment

For each provider A through E:
- **Precision**: What fraction of results are genuinely about the queried company?
  Cite specific false-positive examples.
- **Coverage**: Does it find results for obscure companies (small, non-English,
  low digital profile)? Which companies were missed entirely?
- **Date presence & recency**: Quote the no-date count and the stale (>90d)
  count from the provider header. A provider with many no-date or stale results
  is failing at a basic level — treat it as a major failure, not a minor gripe.
- **Summary usability**: Can the user understand the story without clicking?
  Give a concrete example of a good and bad summary if both exist.
- **Source quality**: Real journalism and press releases are both acceptable.
  Flag aggregators that add no value, product pages, and "About Us" content.
- **Hallucination risk**: Any suspicious URLs or invented facts?
- **Overall verdict**: One frank sentence.

## 2. Ranking (1st to 5th)

Rank all five. For each position give a one-sentence justification. A provider
with a large share of no-date or stale results cannot rank 1st regardless of
other strengths.

## 3. What Each Provider Needs to Fix

For providers ranked 2nd through 5th, list the specific changes needed to
reach 1st place. Distinguish between fixable issues and fundamental problems.

## 4. Top Provider's Weaknesses

List the honest weaknesses of the 1st-ranked provider.
"""

INDUSTRIES_PROMPT = """\
Five news search providers (labelled A–E, real names hidden) were each asked to
return news articles about specific industry/location combinations over the past
3 months.

USER CONTEXT
The user is reviewing industry exposure for internal strategy, supply chain
planning, or sales targeting. They need real strategic developments: pricing
trends, M&A, regulatory shifts, expansion, financial performance for companies
in that industry and geography. They do not want noise.

WHAT COUNTS AS GOOD
- Article or press release containing substantive information relevant to the
  queried industry and geography — it does not have to be exclusively about that
  industry, but the content must be meaningfully informative about it
- Strategic content: pricing trends, M&A, expansion, regulatory shifts, company
  performance within the sector
- Date is present and within the last 90 days (the query window)
- Summary is informative without clicking through
- URL is accessible without a paywall
- No hallucinated content

WHAT COUNTS AS BAD
- Wrong industry: "Film" matched as cinema when searching for packaging film;
  "Distribution" matched as power distribution when searching for media
  distribution services — these are false positives and waste the user's time
- Wrong geography: article is about the industry but in a completely different
  region
- Trivial mentions: the industry or geography appears but nothing useful is
  communicated (e.g., a global market wrap that mentions the region in passing
  with no specific insight)
- "About Us" pages, product catalogues, consumer guides — not news
- Market research report landing pages (pages that sell reports rather than
  containing news)
- **Missing dates** — flagged inline as `[NO DATE ⚠]`. Serious failure: the user
  cannot judge whether the news is current.
- **Stale dates** — flagged inline as `STALE>90d ⚠`. The query window is the
  last 90 days; anything older is off-scope by construction and equivalent to
  a wrong-topic result.
- Raw boilerplate as a summary
- Error rows (failed API calls logged as articles)
- Hallucinated articles

Each provider block's header lists exact counts: `no-date: N | stale (>90d): N`.
Use those numbers — do not estimate.

---

{data}

---

Provide your analysis in this exact structure:

## 1. Provider-by-Provider Assessment

For each provider A through E:
- **Topic relevance**: Are results genuinely about the right industry + location?
  Cite specific false-positive examples (wrong industry, wrong geography).
- **Error rate**: How many results are errors (failed calls)?
- **Coverage breadth**: How many of the 12 topic combinations get real results?
- **Date presence & recency**: Quote the no-date count and the stale (>90d)
  count from the provider header. A provider with many no-date or stale results
  is failing at a basic level — treat it as a major failure, not a minor gripe.
- **Summary usability**: Can the user understand the story without clicking?
- **Source quality**: Real journalism and press releases are both acceptable.
  Flag aggregators that add no value, report landing pages, and product pages.
- **Hallucination risk**: Any suspicious URLs or invented facts?
- **Overall verdict**: One frank sentence.

## 2. Ranking (1st to 5th)

Rank all five. For each position give a one-sentence justification. A provider
with a large share of no-date or stale results cannot rank 1st regardless of
other strengths.

## 3. What Each Provider Needs to Fix

For providers ranked 2nd through 5th, list the specific changes needed to
reach 1st place. Distinguish between fixable issues and fundamental problems.

## 4. Top Provider's Weaknesses

List the honest weaknesses of the 1st-ranked provider.
"""

README_SUMMARY_PROMPT = """\
Two analyses of news search providers are below — one for company queries, one for \
industry/location queries. Providers are coded A–E.

Decode key: {decode_key}

Use real provider names (not coded labels) throughout your response.

Write a short "Results history" entry for a README.md. Output ONLY the entry — no \
preamble, no commentary after. Follow this format exactly:

### {date}

[One sentence: e.g. "Syracuse 1st in both query types:" or \
"No single winner across both query types:"]

- **Companies:** [Provider] 1st (specific reason with concrete examples), \
[Provider] 2nd (reason), [Provider] 3rd (reason), [Provider] 4th (reason), \
[Provider] last (specific failures with examples).
- **Industries:** [Provider] 1st (specific reason), ..., \
[Provider] last (specific failures with examples).

Rules:
- Be specific — name companies that were missed, quote error rates, describe \
hallucination patterns (e.g. "fabricated Reuters/Bloomberg URLs"), note zero-date issues.
- Each bullet is a single sentence covering all five providers in rank order.
- No [Details](...) links.

---
COMPANIES ANALYSIS

{companies_analysis}

---
INDUSTRIES ANALYSIS

{industries_analysis}
"""


# ---------------------------------------------------------------------------
# Data loading and formatting
# ---------------------------------------------------------------------------

def load_csv(filepath: str) -> list[dict]:
    with open(filepath, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def make_anonymization(providers: list[str]) -> tuple[dict, dict]:
    """Randomly assign letters A–E (or more) to provider names.

    Returns (label→provider, provider→label).
    """
    shuffled = providers[:]
    random.shuffle(shuffled)
    letters = list(string.ascii_uppercase[: len(shuffled)])
    label_to_provider = dict(zip(letters, shuffled))
    provider_to_label = {v: k for k, v in label_to_provider.items()}
    return label_to_provider, provider_to_label


def _format_article(index: int, art: dict, reference_date: datetime) -> list[str]:
    lines = []
    bucket = classify_date(art, reference_date)
    if bucket == "no_date":
        date = "NO DATE ⚠"
    else:
        raw = art.get("published_date_clean") or art.get("published_date") or ""
        date = f"{raw} STALE>{STALE_DAYS}d ⚠" if bucket == "stale" else raw
    headline = art.get("headline", "").strip()
    source = art.get("published_by", "").strip()
    url = art.get("document_url", "").strip()
    summary = (art.get("summary_text") or "").strip()
    if len(summary) > MAX_SUMMARY_CHARS:
        summary = summary[:MAX_SUMMARY_CHARS] + "…"

    label_parts = [f"[{date}]", headline]
    if source:
        label_parts.append(f"| {source}")
    lines.append(f"    {index}. {' '.join(label_parts)}")
    if url:
        lines.append(f"       URL: {url}")
    if summary:
        lines.append(f"       {summary}")
    return lines


def _date_counts(arts: list[dict], reference_date: datetime) -> tuple[int, int]:
    no_date = sum(1 for a in arts if classify_date(a, reference_date) == "no_date")
    stale = sum(1 for a in arts if classify_date(a, reference_date) == "stale")
    return no_date, stale


def _group_summary(
    label: str, all_real: list[dict], total_errors: int, reference_date: datetime
) -> list[str]:
    no_date, stale = _date_counts(all_real, reference_date)
    return [
        f"\n{'=' * 60}",
        (
            f"PROVIDER {label}  |  total articles: {len(all_real)}  |  errors: {total_errors}  "
            f"|  no-date: {no_date}  |  stale (>{STALE_DAYS}d): {stale}"
        ),
        "=" * 60,
    ]


def _item_header(kind: str, name: str, real: list[dict], errors: list, reference_date: datetime) -> str:
    no_date, stale = _date_counts(real, reference_date)
    parts = [f"{len(real)} articles"]
    if errors:
        parts.append(f"{len(errors)} errors")
    if no_date:
        parts.append(f"{no_date} no-date")
    if stale:
        parts.append(f"{stale} stale")
    return f"\n  {kind}: {name}  ({', '.join(parts)})"


def format_companies_data(
    rows: list[dict], provider_to_label: dict, max_articles: int, reference_date: datetime
) -> str:
    # Group: label → company → articles
    data: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label = provider_to_label.get(row.get("provider", ""), row.get("provider", ""))
        data[label][row.get("company", "")].append(row)

    lines = []
    for label in sorted(data):
        companies = data[label]
        all_real = [a for arts in companies.values() for a in arts if a.get("headline") != "*** ERROR ***"]
        total_errors = sum(
            len([a for a in arts if a.get("headline") == "*** ERROR ***"])
            for arts in companies.values()
        )
        lines.extend(_group_summary(label, all_real, total_errors, reference_date))

        for company in sorted(companies):
            all_arts = companies[company]
            errors = [a for a in all_arts if a.get("headline") == "*** ERROR ***"]
            real = [a for a in all_arts if a.get("headline") != "*** ERROR ***"]
            real.sort(
                key=lambda x: x.get("published_date_clean") or x.get("published_date") or "",
                reverse=True,
            )
            shown = real[:max_articles]

            lines.append(_item_header("Company", company, real, errors, reference_date))
            if not real:
                lines.append("    [No articles]")
                continue

            for i, art in enumerate(shown, 1):
                lines.extend(_format_article(i, art, reference_date))

            if len(real) > max_articles:
                lines.append(f"    … {len(real) - max_articles} more articles not shown")

    return "\n".join(lines)


def format_industries_data(
    rows: list[dict], provider_to_label: dict, max_articles: int, reference_date: datetime
) -> str:
    # Group: label → topic → articles
    data: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label = provider_to_label.get(row.get("provider", ""), row.get("provider", ""))
        topic = f"{row.get('industry', '')} | {row.get('location', '')}"
        data[label][topic].append(row)

    lines = []
    for label in sorted(data):
        topics = data[label]
        all_real = [a for arts in topics.values() for a in arts if a.get("headline") != "*** ERROR ***"]
        total_errors = sum(
            len([a for a in arts if a.get("headline") == "*** ERROR ***"])
            for arts in topics.values()
        )
        lines.extend(_group_summary(label, all_real, total_errors, reference_date))

        for topic in sorted(topics):
            all_arts = topics[topic]
            errors = [a for a in all_arts if a.get("headline") == "*** ERROR ***"]
            real = [a for a in all_arts if a.get("headline") != "*** ERROR ***"]
            real.sort(
                key=lambda x: x.get("published_date_clean") or x.get("published_date") or "",
                reverse=True,
            )
            shown = real[:max_articles]

            lines.append(_item_header("Topic", topic, real, errors, reference_date))
            if not real:
                lines.append("    [No articles]")
                continue

            for i, art in enumerate(shown, 1):
                lines.extend(_format_article(i, art, reference_date))

            if len(real) > max_articles:
                lines.append(f"    … {len(real) - max_articles} more articles not shown")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_claude(client: anthropic.Anthropic, model: str, data_text: str, prompt_template: str) -> str:
    char_count = len(data_text)
    token_estimate = char_count // 4
    print(f"  Data size: ~{char_count:,} chars / ~{token_estimate:,} tokens")

    user_message = prompt_template.format(data=data_text)
    for attempt in range(4):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            text_block = next(b for b in response.content if b.type == "text")
            return text_block.text
        except anthropic.RateLimitError:
            if attempt == 3:
                raise
            wait = 60 * (attempt + 1)
            print(f"  Rate limit hit — waiting {wait}s before retry {attempt + 2}/4…")
            time.sleep(wait)
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------------------
# README summary
# ---------------------------------------------------------------------------

def generate_readme_summary(
    client: anthropic.Anthropic,
    model: str,
    companies_analysis: str,
    industries_analysis: str,
    label_to_provider: dict,
    run_date: str,
) -> str:
    decode_key = ", ".join(f"{label}={provider}" for label, provider in sorted(label_to_provider.items()))
    prompt = README_SUMMARY_PROMPT.format(
        decode_key=decode_key,
        date=run_date,
        companies_analysis=companies_analysis,
        industries_analysis=industries_analysis,
    )
    for attempt in range(4):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            text_block = next(b for b in response.content if b.type == "text")
            return text_block.text
        except anthropic.RateLimitError:
            if attempt == 3:
                raise
            wait = 60 * (attempt + 1)
            print(f"  Rate limit hit — waiting {wait}s before retry {attempt + 2}/4…")
            time.sleep(wait)
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run(results_dir: str, output_dir: str | None = None, model: str = DEFAULT_MODEL, max_articles: int = DEFAULT_MAX_ARTICLES):
    if output_dir is None:
        output_dir = results_dir

    companies_csv = os.path.join(results_dir, "companies.csv")
    industries_csv = os.path.join(results_dir, "industries.csv")

    missing = [p for p in (companies_csv, industries_csv) if not os.path.exists(p)]
    if missing:
        raise FileNotFoundError(f"Missing expected files: {missing}")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set in environment / .env")

    companies_rows = load_csv(companies_csv)
    industries_rows = load_csv(industries_csv)

    providers = sorted(
        {r["provider"] for r in companies_rows + industries_rows if r.get("provider")}
    )
    print(f"Providers found: {providers}")

    # Anonymize
    label_to_provider, provider_to_label = make_anonymization(providers)
    print(f"Anonymization mapping (hidden from model): {label_to_provider}\n")

    client = anthropic.Anthropic(api_key=api_key)

    reference_date = reference_date_from_results_dir(results_dir)
    print(f"Recency reference date (from results dir): {reference_date.date()}  "
          f"| stale threshold: >{STALE_DAYS} days")

    # Companies analysis
    print("Formatting companies data…")
    companies_data = format_companies_data(companies_rows, provider_to_label, max_articles, reference_date)

    print("Calling Claude for companies analysis…")
    companies_analysis = call_claude(client, model, companies_data, COMPANIES_PROMPT)

    # Pause to avoid hitting the per-minute token rate limit between the two calls
    print("\nWaiting 60s to stay within token-per-minute rate limit…")
    time.sleep(60)

    # Industries analysis
    print("\nFormatting industries data…")
    industries_data = format_industries_data(industries_rows, provider_to_label, max_articles, reference_date)

    print("Calling Claude for industries analysis…")
    industries_analysis = call_claude(client, model, industries_data, INDUSTRIES_PROMPT)

    # Save
    ai_dir = os.path.join(output_dir, "AI-analysis")
    os.makedirs(ai_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    key_path = os.path.join(ai_dir, f"decode-key-{timestamp}.json")
    with open(key_path, "w") as f:
        json.dump(
            {
                "label_to_provider": label_to_provider,
                "provider_to_label": provider_to_label,
                "model": model,
                "max_articles_per_item": max_articles,
                "generated_at": timestamp,
            },
            f,
            indent=2,
        )

    companies_path = os.path.join(ai_dir, f"claude-companies-{timestamp}.md")
    with open(companies_path, "w") as f:
        f.write(f"# Companies Analysis — {timestamp}\n\n")
        f.write(f"*Model: {model} | Max articles per company per provider: {max_articles}*\n\n")
        f.write(f"*Provider labels were anonymised. See `decode-key-{timestamp}.json` to decode.*\n\n")
        f.write("---\n\n")
        f.write(companies_analysis)

    industries_path = os.path.join(ai_dir, f"claude-industries-{timestamp}.md")
    with open(industries_path, "w") as f:
        f.write(f"# Industries Analysis — {timestamp}\n\n")
        f.write(f"*Model: {model} | Max articles per topic per provider: {max_articles}*\n\n")
        f.write(f"*Provider labels were anonymised. See `decode-key-{timestamp}.json` to decode.*\n\n")
        f.write("---\n\n")
        f.write(industries_analysis)

    print(f"\nResults saved to:")
    print(f"  {companies_path}")
    print(f"  {industries_path}")
    print(f"  {key_path}")
    print(f"\nDecode key:")
    for label, provider in sorted(label_to_provider.items()):
        print(f"  Provider {label} = {provider}")

    # Generate README snippet
    print("\nWaiting 60s before README summary to stay within token-per-minute rate limit…")
    time.sleep(60)
    print("Generating README summary…")
    run_date = os.path.basename(os.path.normpath(results_dir))
    readme_summary = generate_readme_summary(
        client, model, companies_analysis, industries_analysis, label_to_provider, run_date
    )
    print("\n" + "=" * 60)
    print("README SNIPPET — paste into Results history in README.md")
    print("=" * 60)
    print(readme_summary)
    print("=" * 60)


def run_readme_only(results_dir: str, model: str = DEFAULT_MODEL):
    """Generate a README snippet from existing AI-analysis files without re-running analysis."""
    ai_dir = os.path.join(results_dir, "AI-analysis")
    if not os.path.isdir(ai_dir):
        raise FileNotFoundError(f"No AI-analysis directory found in {results_dir}")

    key_files = sorted(f for f in os.listdir(ai_dir) if f.startswith("decode-key-") and f.endswith(".json"))
    if not key_files:
        raise FileNotFoundError(f"No decode-key-*.json files found in {ai_dir}")

    key_path = os.path.join(ai_dir, key_files[-1])
    print(f"Using decode key: {key_path}")
    with open(key_path) as f:
        key_data = json.load(f)

    label_to_provider = key_data["label_to_provider"]
    timestamp = key_data["generated_at"]

    companies_path = os.path.join(ai_dir, f"claude-companies-{timestamp}.md")
    industries_path = os.path.join(ai_dir, f"claude-industries-{timestamp}.md")
    for p in (companies_path, industries_path):
        if not os.path.exists(p):
            raise FileNotFoundError(f"Expected analysis file not found: {p}")

    with open(companies_path) as f:
        companies_analysis = f.read()
    with open(industries_path) as f:
        industries_analysis = f.read()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set in environment / .env")

    client = anthropic.Anthropic(api_key=api_key)
    run_date = os.path.basename(os.path.normpath(results_dir))

    print("Generating README summary…")
    readme_summary = generate_readme_summary(
        client, model, companies_analysis, industries_analysis, label_to_provider, run_date
    )
    print("\n" + "=" * 60)
    print("README SNIPPET — paste into Results history in README.md")
    print("=" * 60)
    print(readme_summary)
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Analyse provider comparison results with Claude (anonymised)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s results/2026-03-02
  %(prog)s results/2026-03-02 --model claude-sonnet-4-6
  %(prog)s results/2026-03-02 --max-articles 20
  %(prog)s results/2026-03-02 --readme-only
        """,
    )
    parser.add_argument(
        "results_dir",
        help="Directory containing companies.csv and industries.csv",
    )
    parser.add_argument(
        "--output-dir",
        help="Where to write analysis files (defaults to results_dir)",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--max-articles",
        type=int,
        default=DEFAULT_MAX_ARTICLES,
        help=f"Max articles per company/topic per provider sent to the model (default: {DEFAULT_MAX_ARTICLES})",
    )
    parser.add_argument(
        "--readme-only",
        action="store_true",
        help="Skip analysis; generate README snippet from existing AI-analysis files",
    )
    args = parser.parse_args()
    if args.readme_only:
        run_readme_only(args.results_dir, args.model)
    else:
        run(args.results_dir, args.output_dir, args.model, args.max_articles)


if __name__ == "__main__":
    main()
