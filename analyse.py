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
import re
import string
import time
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

import anthropic
from dotenv import load_dotenv

load_dotenv()

DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_MAX_ARTICLES = 15   # per company/topic per provider
MAX_SUMMARY_CHARS = 200     # truncate summaries to keep prompt manageable
STALE_DAYS = 90             # articles older than this are flagged as stale

# Rubric: five axes summing to 1.0. Tuneable in one place.
RUBRIC_WEIGHTS = {
    "precision":         0.35,
    "coverage":          0.20,
    "recency_integrity": 0.15,
    "story_quality":     0.15,
    "trust":             0.15,
}
RUBRIC_AXES = list(RUBRIC_WEIGHTS.keys())

# Hard caps on the final score. Encode the user's stated priorities directly:
# false positives, missing dates, and hallucinations cannot be outweighed by
# strength on other axes.
CAP_RECENCY_HARD_THRESHOLD = 3   # recency_integrity ≤ 3
CAP_RECENCY_HARD_LIMIT     = 5.0
CAP_RECENCY_SOFT_THRESHOLD = 5   # recency_integrity ≤ 5
CAP_RECENCY_SOFT_LIMIT     = 7.0
CAP_TRUST_THRESHOLD        = 4   # trust ≤ 4
CAP_TRUST_LIMIT            = 4.0
CAP_PRECISION_THRESHOLD    = 3   # precision ≤ 3
CAP_PRECISION_LIMIT        = 5.0


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


_HEADLINE_STEM_RE = re.compile(r"[^a-z0-9]+")


def _normalise_url(url: str) -> str:
    """Canonical URL key: lowercase host, drop fragment and tracking params."""
    if not url:
        return ""
    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return url.strip().lower()
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    query = [
        (k, v)
        for k, v in parse_qsl(parts.query, keep_blank_values=True)
        if not k.lower().startswith("utm_")
    ]
    return urlunsplit((parts.scheme.lower(), host, parts.path.rstrip("/"), urlencode(query), ""))


def _headline_stem(headline: str) -> str:
    """First 60 chars of lowercased, alphanumerics-only headline."""
    return _HEADLINE_STEM_RE.sub("", (headline or "").lower())[:60]


def _compute_dup_groups(articles: list[dict]) -> list[int]:
    """Assign a 1-based group id per article. Articles in the same group are
    duplicates: same canonical URL, or (failing that) same source+headline-stem.
    Returns a list parallel to ``articles``."""
    url_to_group: dict[str, int] = {}
    pair_to_group: dict[tuple[str, str], int] = {}
    groups: list[int] = []
    next_id = 1
    for art in articles:
        url_key = _normalise_url(art.get("document_url", ""))
        if url_key and url_key in url_to_group:
            groups.append(url_to_group[url_key])
            continue
        stem_key = (
            (art.get("published_by") or "").strip().lower(),
            _headline_stem(art.get("headline", "")),
        )
        if stem_key[1] and stem_key in pair_to_group:
            gid = pair_to_group[stem_key]
            groups.append(gid)
            if url_key:
                url_to_group[url_key] = gid
            continue
        gid = next_id
        next_id += 1
        groups.append(gid)
        if url_key:
            url_to_group[url_key] = gid
        if stem_key[1]:
            pair_to_group[stem_key] = gid
    return groups


def _dup_count(groups: list[int]) -> int:
    """Number of duplicate articles (i.e. excess rows beyond one canonical per group)."""
    return len(groups) - len(set(groups))


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
You are a ruthlessly objective product quality analyst evaluating news search
providers against a fixed rubric. Your output drives a numeric scorecard, not
a prose review.

Non-negotiable rules:
1. Score every provider on every axis (precision, coverage, recency_integrity,
   story_quality, trust). Use the full 0–10 range. A 7 across the board
   is a refusal to judge — if the data shows a 3, write 3. Refusing to
   differentiate is itself a failure mode.
2. Every axis score must be backed by concrete evidence as an array of short
   strings. Each evidence string must name a queried entity (company name, or
   industry+location) and quote a headline, source, or pattern. Generic claims
   like "many results were off-topic" without examples are malformed and will
   be rejected.
3. Pre-computed flags in the data are ground truth — use them directly:
     - `[NO DATE ⚠]` and `STALE>90d ⚠` drive recency_integrity.
     - `[DUP of #N ⚠]` flags and the `dup: N` count in each provider header
       drive uniqueness.
     - `*** ERROR ***` rows and the `errors: N` header count drive trust.
   Do not re-judge dates or re-detect duplicates. Quote the header counts.
4. The rubric prioritises avoiding false positives over finding every story.
   A provider that returns 5 clean on-topic articles beats one that returns
   30 articles half of which are wrong-entity, About Us pages, or social
   posts. Reflect this in precision.
5. You do not know who built any of these providers. Treat A, B, C, D, E as
   interchangeable labels. Score on the data alone.
6. Output exactly the JSON scorecard schema given, inside a single ```json
   fenced block, followed by a short ## Notes prose section. Do not add
   fields, do not omit fields, do not put commentary inside the JSON block.
"""

_RUBRIC_BLOCK = """\
RUBRIC

Score each provider on these five 0–10 axes. Weights are fixed (sum to 1.0):

| Axis              | Weight | What 10 looks like                                      | What 0 looks like                                               |
|-------------------|--------|---------------------------------------------------------|-----------------------------------------------------------------|
| precision         | 0.35   | 100% of returned articles are relevant and on-topic. **No results → score 0** | Any off-topic, wrong-entity, not-news, or stale content; or no results returned |
| coverage          | 0.20   | At least one real, relevant article for nearly every queried entity | Multiple queried entities return no results at all      |
| recency_integrity | 0.15   | 0 no-date, 0 stale (header counts)                     | Large no-date or stale share                                    |
| story_quality     | 0.15   | Summaries let user decide without clicking              | Boilerplate, cookie banners, "subscribe to read"                |
| trust             | 0.15   | 0 errors, no suspicious URLs                            | Hallucinated URLs/facts; high error rate                        |

For each axis, output a 0–10 score and an `evidence` array of 1–4 short strings.
Each evidence string MUST name a queried entity (or industry+location) and quote
a specific headline, source, or counted pattern. Anonymous claims are malformed.

SCORING — COMPUTED BY THE HARNESS, NOT BY YOU
Your axis scores are the only scoring input. After you respond, the harness
computes, for each provider:
  weighted = 0.35·precision + 0.20·coverage + 0.15·recency_integrity
           + 0.15·story_quality + 0.15·trust
  hard caps: recency_integrity ≤ 3 → final ≤ 5.0; recency_integrity ≤ 5 →
  final ≤ 7.0; trust ≤ 4 → final ≤ 4.0; precision ≤ 3 → final ≤ 5.0
  final = min(weighted, applicable caps); ranking = final descending, ties
  broken by precision then recency_integrity.
Do NOT compute or output weighted, final, caps, a ranking, or any claim about
which provider is best overall — LLM arithmetic is unreliable and any ordering
you state will be discarded. Score each axis on its own merits.

OUTPUT SCHEMA — emit exactly one ```json fenced block, then a `## Notes`
section. No prose inside the JSON block.

```json
{
  "query_type": "__QUERY_TYPE__",
  "providers": [
    {
      "label": "A",
      "axes": {
        "precision":         {"score": 0, "evidence": ["..."]},
        "coverage":          {"score": 0, "evidence": ["..."]},
        "recency_integrity": {"score": 0, "evidence": ["..."]},
        "story_quality":     {"score": 0, "evidence": ["..."]},
        "trust":             {"score": 0, "evidence": ["..."]}
      },
      "verdict": "one frank sentence about this provider's own strengths and weaknesses — no rank claims"
    }
  ]
}
```

After the JSON block, write a `## Notes` heading and 1–2 short paragraphs:
surprising patterns across the run, and the honest weaknesses of whichever
provider(s) look strongest on the axes. Do not declare a winner or an
ordering — the harness computes the official ranking from your axis scores.
"""

COMPANIES_PROMPT = """\
Five news search providers (labelled A–E, real names hidden) were each asked to
return news articles about specific companies over the past 90 days.

USER CONTEXT
The consumer is either a human business professional or an AI agent that just
needs recent (last 90 days) news about the queried company. They already have
other data sources for company registration, statutory filings, and profile
data. This tool only needs to surface recent news. False positives mislead an
AI agent and waste a human's time, so they are the top concern. False negatives
matter less.

WHAT COUNTS AS GOOD (TP)
- Real article or press release with substantive information about the queried
  company (M&A, financials, product launches, regulatory matters, executive
  moves, expansion). The company need not be the sole subject, but the mention
  must be informative, not a name-drop.
- Date present and within the last 90 days.
- Summary informative enough to decide whether to click through.
- URL accessible.
- English language (non-English content for a non-local company is a wrong-
  region signal — count as FP-entity).

WHAT COUNTS AS BAD (FP)
- FP-entity: wrong company that merely shares part of a name (e.g. "Sigma
  Lithium" returned for "Sigma Chemtrade"); macro market roundups that
  name-drop the company alongside dozens of others with no specific information
  about it; broader-than-asked content (industry-level when a company was
  asked).
- FP-not-news: About Us pages, product catalogues, consumer how-to guides,
  company registration / registry / directory listings, social media posts
  (Facebook, X/Twitter, LinkedIn, Reddit, YouTube, TikTok), forum threads,
  personal blogs.
- FP-stale / FP-no-date: flagged inline as `STALE>90d ⚠` and `[NO DATE ⚠]`.
  Treat as off-scope (header counts are ground truth — quote them).
- FP-dup: flagged inline as `[DUP of #N ⚠]`; header `dup: N` is ground truth.
- FP-halluc: suspiciously neat URL patterns that don't correspond to real
  published content; invented facts.
- Raw scraped boilerplate as a "summary" (cookie banners, "Are you a robot",
  navigation menus).

NOTE on market-report landing pages: for a company query they are typically
off-topic noise — count as FP-not-news.

__RUBRIC__

---

__DATA__

---
"""

INDUSTRIES_PROMPT = """\
Five news search providers (labelled A–E, real names hidden) were each asked to
return news articles about specific industry/location combinations over the
past 90 days.

USER CONTEXT
The consumer is either a human business professional or an AI agent reviewing
industry exposure (strategy, supply chain, sales targeting). They need real
strategic developments — pricing trends, M&A, regulatory shifts, expansion,
financial performance — for the queried industry in the queried geography.
False positives are the top concern; false negatives matter less.

WHAT COUNTS AS GOOD (TP)
- Article or press release with substantive information about the queried
  industry in the queried geography. Not exclusively about that industry, but
  meaningfully informative.
- Date present and within the last 90 days.
- Summary informative enough to decide whether to click through.
- URL accessible.
- English language.

WHAT COUNTS AS BAD (FP)
- FP-entity (wrong topic / region): "Film" matched as cinema when packaging
  film was asked; "Distribution" matched as power distribution when media
  distribution was asked; right industry but completely different region;
  global market wraps that mention the region in passing with no specific
  insight; broader-than-asked content (different industry segment, or
  worldwide when a region was asked).
- FP-not-news: About Us pages, product catalogues, consumer guides, company
  registration / registry / directory listings, social media posts, forum
  threads, personal blogs.
- FP-stale / FP-no-date / FP-dup: see header counts (ground truth).
- FP-halluc: suspicious URL patterns; invented facts.
- Errors: `*** ERROR ***` rows — header `errors: N` is ground truth.

NOTE on market-report landing pages: a small number (≤2 per topic) provides
useful state-of-market context — count those as on-topic (TP / TP-thin). Beyond
that, surplus copies are noise — count the excess as FP-not-news. Do not
blanket-penalise.

__RUBRIC__

---

__DATA__

---
"""


def _build_prompt(template: str, query_type: str) -> str:
    return template.replace("__RUBRIC__", _RUBRIC_BLOCK).replace("__QUERY_TYPE__", query_type)


COMPANIES_PROMPT = _build_prompt(COMPANIES_PROMPT, "companies")
INDUSTRIES_PROMPT = _build_prompt(INDUSTRIES_PROMPT, "industries")

README_SUMMARY_PROMPT = """\
Two scorecards are below — one for company queries, one for industry/location
queries. Providers are coded A–E.

Decode key: __DECODE_KEY__

Use real provider names (not coded labels) throughout your response.

Write a short "Results history" entry for a README.md. Output ONLY the entry —
no preamble, no commentary after. Follow this format exactly:

### __DATE__

__HEADLINE__

- **Companies:** [Provider] 1st (final/10 — one-clause reason with a concrete
  example), [Provider] 2nd (final/10 — reason), [Provider] 3rd (final/10 — reason),
  [Provider] 4th (final/10 — reason), [Provider] last (final/10 — specific failure).
- **Industries:** [Provider] 1st (final/10 — reason), …, [Provider] last
  (final/10 — specific failure).

**Recommendation for autonomous use** (agent or human acting without manual filtering):

- **Companies:** [one of the three verdicts below — use real provider names]
- **Industries:** [one of the three verdicts below — use real provider names]

Verdict options (pick exactly one per use case):
1. **Use [Provider]** — top provider's final ≥ 6.0 AND precision ≥ 6 AND no trust
   or precision cap engaged. One clause explaining why it clears the bar.
2. **Use [Provider] + [Provider]** — no single provider clears the bar alone, but
   combining the top-precision provider (for signal quality) with the top-coverage
   provider (for breadth) is net-positive. Only recommend this if both have
   precision ≥ 5 and neither has a trust cap. One clause on what each contributes.
3. **None suitable for autonomous use** — no provider clears the precision ≥ 5 and
   final ≥ 5 threshold needed for unfiltered agent use. One clause naming the
   dominant failure mode (e.g. "high false-positive rate across all providers").

Rules:
- The headline sentence under the date was computed programmatically from the
  rankings — reproduce it verbatim as the first line of the entry. Do not
  reword it, embellish it, or contradict it.
- The `final`, `weighted`, `caps_applied`, and `ranking` fields were computed
  programmatically from the axis scores and are ground truth. List providers in
  each bullet strictly in `ranking` array order, quoting the `final` values as
  given. If verdicts or notes prose imply a different order, the prose is stale
  — the JSON numbers win.
- Quote each provider's `final` score (one decimal place, out of 10) in parens.
- If a provider has any entries in `caps_applied`, mention the engaged cap
  (e.g. "recency cap" or "trust cap") and the underlying reason (e.g. "12 no-date
  results", "fabricated Reuters URLs").
- Be specific — name a queried entity from `evidence` to back the reason.
- Each ranking bullet is a single sentence covering all five providers in rank order
  (use the `ranking` array).
- No [Details](...) links.

---
COMPANIES SCORECARD (JSON)

```json
__COMPANIES_SCORECARD__
```

---
INDUSTRIES SCORECARD (JSON)

```json
__INDUSTRIES_SCORECARD__
```

---
COMPANIES NOTES (prose excerpt for color)

__COMPANIES_NOTES__

---
INDUSTRIES NOTES (prose excerpt for color)

__INDUSTRIES_NOTES__
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


def _format_article(
    index: int, art: dict, reference_date: datetime, dup_marker: str = ""
) -> list[str]:
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

    label_parts = [f"[{date}]"]
    if dup_marker:
        label_parts.append(f"[{dup_marker} ⚠]")
    label_parts.append(headline)
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
    label: str,
    all_real: list[dict],
    total_errors: int,
    reference_date: datetime,
    total_dups: int,
) -> list[str]:
    no_date, stale = _date_counts(all_real, reference_date)
    return [
        f"\n{'=' * 60}",
        (
            f"PROVIDER {label}  |  total articles: {len(all_real)}  |  errors: {total_errors}  "
            f"|  no-date: {no_date}  |  stale (>{STALE_DAYS}d): {stale}  |  dup: {total_dups}"
        ),
        "=" * 60,
    ]


def _item_header(
    kind: str,
    name: str,
    real: list[dict],
    errors: list,
    reference_date: datetime,
    dup: int,
) -> str:
    no_date, stale = _date_counts(real, reference_date)
    parts = [f"{len(real)} articles"]
    if errors:
        parts.append(f"{len(errors)} errors")
    if no_date:
        parts.append(f"{no_date} no-date")
    if stale:
        parts.append(f"{stale} stale")
    if dup:
        parts.append(f"{dup} dup")
    return f"\n  {kind}: {name}  ({', '.join(parts)})"


def _render_item(
    kind: str,
    name: str,
    real: list[dict],
    errors: list,
    reference_date: datetime,
    max_articles: int,
) -> tuple[list[str], int]:
    """Render one item (company or topic). Returns (lines, dup_count_for_this_item)."""
    real_sorted = sorted(
        real,
        key=lambda x: x.get("published_date_clean") or x.get("published_date") or "",
        reverse=True,
    )
    groups = _compute_dup_groups(real_sorted)
    item_dup = _dup_count(groups)

    shown = real_sorted[:max_articles]
    shown_groups = groups[: len(shown)]
    canonical_pos: dict[int, int] = {}
    for i, gid in enumerate(shown_groups, 1):
        canonical_pos.setdefault(gid, i)

    lines = [_item_header(kind, name, real_sorted, errors, reference_date, item_dup)]
    if not real_sorted:
        lines.append("    [No articles]")
        return lines, item_dup

    for i, (art, gid) in enumerate(zip(shown, shown_groups), 1):
        canon = canonical_pos[gid]
        marker = f"DUP of #{canon}" if canon != i else ""
        lines.extend(_format_article(i, art, reference_date, marker))

    if len(real_sorted) > max_articles:
        lines.append(f"    … {len(real_sorted) - max_articles} more articles not shown")

    return lines, item_dup


def format_companies_data(
    rows: list[dict], provider_to_label: dict, max_articles: int, reference_date: datetime
) -> str:
    # Group: label → company → articles
    data: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label = provider_to_label.get(row.get("provider", ""), row.get("provider", ""))
        data[label][row.get("company", "")].append(row)

    return _format_grouped("Company", data, reference_date, max_articles)


def format_industries_data(
    rows: list[dict], provider_to_label: dict, max_articles: int, reference_date: datetime
) -> str:
    # Group: label → topic → articles
    data: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label = provider_to_label.get(row.get("provider", ""), row.get("provider", ""))
        topic = f"{row.get('industry', '')} | {row.get('location', '')}"
        data[label][topic].append(row)

    return _format_grouped("Topic", data, reference_date, max_articles)


def _format_grouped(
    kind: str,
    data: dict[str, dict[str, list[dict]]],
    reference_date: datetime,
    max_articles: int,
) -> str:
    lines: list[str] = []
    for label in sorted(data):
        items = data[label]
        all_real = [
            a
            for arts in items.values()
            for a in arts
            if a.get("headline") != "*** ERROR ***"
        ]
        total_errors = sum(
            len([a for a in arts if a.get("headline") == "*** ERROR ***"])
            for arts in items.values()
        )

        # First render each item to get per-item dup counts; then prepend the
        # provider header with the aggregate dup total.
        item_blocks: list[list[str]] = []
        total_dups = 0
        for name in sorted(items):
            all_arts = items[name]
            errors = [a for a in all_arts if a.get("headline") == "*** ERROR ***"]
            real = [a for a in all_arts if a.get("headline") != "*** ERROR ***"]
            block, item_dup = _render_item(
                kind, name, real, errors, reference_date, max_articles
            )
            total_dups += item_dup
            item_blocks.append(block)

        lines.extend(_group_summary(label, all_real, total_errors, reference_date, total_dups))
        for block in item_blocks:
            lines.extend(block)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def call_claude(client: anthropic.Anthropic, model: str, data_text: str, prompt_template: str) -> str:
    char_count = len(data_text)
    token_estimate = char_count // 4
    print(f"  Data size: ~{char_count:,} chars / ~{token_estimate:,} tokens")

    user_message = prompt_template.replace("__DATA__", data_text)
    for attempt in range(4):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=12288,
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
# Scorecard parsing
# ---------------------------------------------------------------------------

_JSON_BLOCK_RE = re.compile(r"```json\s*\n(.*?)\n```", re.S)
_NOTES_RE = re.compile(r"##\s*Notes\s*\n(.*?)\Z", re.S)


def _apply_caps(axes: dict, weighted: float) -> tuple[float, list[str]]:
    """Recompute final score and engaged caps from axis scores."""
    caps: list[str] = []
    final = weighted
    rec = axes["recency_integrity"]["score"]
    trust = axes["trust"]["score"]
    prec = axes["precision"]["score"]
    if rec <= CAP_RECENCY_HARD_THRESHOLD:
        caps.append("recency_hard")
        final = min(final, CAP_RECENCY_HARD_LIMIT)
    elif rec <= CAP_RECENCY_SOFT_THRESHOLD:
        caps.append("recency_soft")
        final = min(final, CAP_RECENCY_SOFT_LIMIT)
    if trust <= CAP_TRUST_THRESHOLD:
        caps.append("trust")
        final = min(final, CAP_TRUST_LIMIT)
    if prec <= CAP_PRECISION_THRESHOLD:
        caps.append("precision")
        final = min(final, CAP_PRECISION_LIMIT)
    return round(final, 2), caps


def _recompute_provider(provider: dict) -> dict:
    """Recompute weighted, final, caps_applied from axis scores. Mutates and returns."""
    axes = provider["axes"]
    missing = [a for a in RUBRIC_AXES if a not in axes]
    if missing:
        raise ValueError(f"Provider {provider.get('label', '?')} missing axes: {missing}")
    weighted = sum(RUBRIC_WEIGHTS[a] * axes[a]["score"] for a in RUBRIC_AXES)
    weighted = round(weighted, 2)
    final, caps = _apply_caps(axes, weighted)

    model_weighted = provider.get("weighted")
    model_final = provider.get("final")
    if model_weighted is not None and abs(model_weighted - weighted) > 0.05:
        print(f"  ⚠ Provider {provider.get('label')}: weighted recomputed "
              f"{weighted} vs model {model_weighted}; using recomputed.")
    if model_final is not None and abs(model_final - final) > 0.05:
        print(f"  ⚠ Provider {provider.get('label')}: final recomputed "
              f"{final} vs model {model_final}; using recomputed.")

    provider["weighted"] = weighted
    provider["final"] = final
    provider["caps_applied"] = caps
    return provider


def parse_scorecard(analysis_text: str) -> dict:
    """Extract the fenced JSON scorecard, validate axes, recompute scores
    server-side, and re-derive the ranking from the recomputed final scores."""
    match = _JSON_BLOCK_RE.search(analysis_text)
    if not match:
        raise ValueError("No ```json fenced block found in analysis output")
    data = json.loads(match.group(1))
    if "providers" not in data:
        raise ValueError("Scorecard JSON missing 'providers' key")
    for prov in data["providers"]:
        for axis in RUBRIC_AXES:
            score = prov.get("axes", {}).get(axis, {}).get("score")
            if not isinstance(score, (int, float)) or not 0 <= score <= 10:
                raise ValueError(
                    f"Provider {prov.get('label')} axis {axis} has invalid score: {score!r}"
                )
        _recompute_provider(prov)

    data["providers"].sort(
        key=lambda p: (
            -p["final"],
            -p["axes"]["precision"]["score"],
            -p["axes"]["recency_integrity"]["score"],
        )
    )
    data["ranking"] = [p["label"] for p in data["providers"]]
    # Any model-authored ranking or rationale reflects its own (unreliable)
    # arithmetic and may contradict the recomputed ranking — discard it.
    data.pop("ranking_rationale", None)
    return data


def extract_notes(analysis_text: str) -> str:
    match = _NOTES_RE.search(analysis_text)
    return match.group(1).strip() if match else ""


# ---------------------------------------------------------------------------
# README summary
# ---------------------------------------------------------------------------

def _headline_sentence(
    companies_scorecard: dict, industries_scorecard: dict, label_to_provider: dict
) -> str:
    """Derive the headline result from the recomputed rankings — never from
    the model, whose prose has previously contradicted the ranking arrays."""
    companies_winner = label_to_provider[companies_scorecard["ranking"][0]]
    industries_winner = label_to_provider[industries_scorecard["ranking"][0]]
    if companies_winner == industries_winner:
        return f"{companies_winner} 1st in both query types."
    return (
        f"No single winner: {companies_winner} 1st for companies, "
        f"{industries_winner} 1st for industries."
    )


def generate_readme_summary(
    client: anthropic.Anthropic,
    model: str,
    companies_scorecard: dict,
    industries_scorecard: dict,
    companies_notes: str,
    industries_notes: str,
    label_to_provider: dict,
    run_date: str,
) -> str:
    decode_key = ", ".join(
        f"{label}={provider}" for label, provider in sorted(label_to_provider.items())
    )
    # Older scorecards carry a model-authored ranking_rationale keyed by
    # position; it can contradict the recomputed ranking — never show it.
    companies_scorecard = {k: v for k, v in companies_scorecard.items() if k != "ranking_rationale"}
    industries_scorecard = {k: v for k, v in industries_scorecard.items() if k != "ranking_rationale"}
    headline = _headline_sentence(companies_scorecard, industries_scorecard, label_to_provider)
    prompt = (
        README_SUMMARY_PROMPT
        .replace("__DECODE_KEY__", decode_key)
        .replace("__DATE__", run_date)
        .replace("__HEADLINE__", headline)
        .replace("__COMPANIES_SCORECARD__", json.dumps(companies_scorecard, indent=2))
        .replace("__INDUSTRIES_SCORECARD__", json.dumps(industries_scorecard, indent=2))
        .replace("__COMPANIES_NOTES__", companies_notes or "(none)")
        .replace("__INDUSTRIES_NOTES__", industries_notes or "(none)")
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

    # Parse and recompute server-side
    print("\nParsing scorecards…")
    companies_scorecard = parse_scorecard(companies_analysis)
    industries_scorecard = parse_scorecard(industries_analysis)
    companies_notes = extract_notes(companies_analysis)
    industries_notes = extract_notes(industries_analysis)

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

    companies_json_path = os.path.join(ai_dir, f"claude-companies-{timestamp}.json")
    with open(companies_json_path, "w") as f:
        json.dump(companies_scorecard, f, indent=2)

    industries_json_path = os.path.join(ai_dir, f"claude-industries-{timestamp}.json")
    with open(industries_json_path, "w") as f:
        json.dump(industries_scorecard, f, indent=2)

    print(f"\nResults saved to:")
    print(f"  {companies_path}")
    print(f"  {industries_path}")
    print(f"  {companies_json_path}")
    print(f"  {industries_json_path}")
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
        client,
        model,
        companies_scorecard,
        industries_scorecard,
        companies_notes,
        industries_notes,
        label_to_provider,
        run_date,
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

    companies_md_path = os.path.join(ai_dir, f"claude-companies-{timestamp}.md")
    industries_md_path = os.path.join(ai_dir, f"claude-industries-{timestamp}.md")
    companies_json_path = os.path.join(ai_dir, f"claude-companies-{timestamp}.json")
    industries_json_path = os.path.join(ai_dir, f"claude-industries-{timestamp}.json")
    for p in (companies_md_path, industries_md_path):
        if not os.path.exists(p):
            raise FileNotFoundError(f"Expected analysis file not found: {p}")

    with open(companies_md_path) as f:
        companies_md = f.read()
    with open(industries_md_path) as f:
        industries_md = f.read()

    # Prefer pre-parsed JSON sidecars; fall back to extracting from markdown
    # for older runs that pre-date the JSON output.
    if os.path.exists(companies_json_path):
        with open(companies_json_path) as f:
            companies_scorecard = json.load(f)
    else:
        companies_scorecard = parse_scorecard(companies_md)
    if os.path.exists(industries_json_path):
        with open(industries_json_path) as f:
            industries_scorecard = json.load(f)
    else:
        industries_scorecard = parse_scorecard(industries_md)

    companies_notes = extract_notes(companies_md)
    industries_notes = extract_notes(industries_md)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY is not set in environment / .env")

    client = anthropic.Anthropic(api_key=api_key)
    run_date = os.path.basename(os.path.normpath(results_dir))

    print("Generating README summary…")
    readme_summary = generate_readme_summary(
        client,
        model,
        companies_scorecard,
        industries_scorecard,
        companies_notes,
        industries_notes,
        label_to_provider,
        run_date,
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
