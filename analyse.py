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
import statistics
import string
import time
import unicodedata
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

import anthropic
from dotenv import load_dotenv
from utils import publisher_domain

load_dotenv()

DEFAULT_MODEL = "claude-opus-4-7"
DEFAULT_MAX_ARTICLES = 15   # per company/topic per provider
MAX_SUMMARY_CHARS = 200     # truncate summaries to keep prompt manageable
STALE_DAYS = 90             # articles older than this are flagged as stale

# Rubric: five axes summing to 1.0. Tuneable in one place.
RUBRIC_WEIGHTS = {
    "precision":          0.35,
    "coverage":           0.20,
    "metadata_integrity": 0.15,
    "story_quality":      0.15,
    "trust":              0.15,
}
RUBRIC_AXES = list(RUBRIC_WEIGHTS.keys())

# Hard caps on the final score. Encode the user's stated priorities directly:
# false positives, missing dates, missing publishers, and hallucinations cannot
# be outweighed by strength on other axes.
CAP_METADATA_HARD_THRESHOLD = 3   # metadata_integrity ≤ 3
CAP_METADATA_HARD_LIMIT     = 5.0
CAP_METADATA_SOFT_THRESHOLD = 5   # metadata_integrity ≤ 5
CAP_METADATA_SOFT_LIMIT     = 7.0
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


def article_domain(art: dict) -> str:
    """Domain of the article URL. Prefer the column written by main.py; derive it
    for older results files that predate that column."""
    stored = (art.get("publisher_domain") or "").strip()
    return stored or publisher_domain(art.get("document_url", ""))


def classify_publisher(art: dict) -> str:
    """Return "no_publisher" or "published", based only on the publisher name the
    provider actually supplied. The domain is not a substitute: it is derivable
    from any URL, so crediting it would score every provider identically and
    measure nothing. It is shown to the judge alongside, which is why a missing
    publisher weighs less than a missing date."""
    return "published" if (art.get("published_by") or "").strip() else "no_publisher"


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


# Market-research-report landing pages / SEO announcements ("X Market to Reach
# USD Y Billion by 2034 at Z% CAGR"). Flagged so the judge gets ground-truth
# counts instead of re-detecting them inconsistently each run.
_MARKET_REPORT_RE = re.compile(
    r"\bCAGR\b"
    r"|\bmarkets?\b[^.]{0,60}?\b(size|share|growth|forecast\w*|outlook|report\w*|"
    r"analysis|trends?|opportunit\w*|to reach|reach(es|ing)?|projected|poised|"
    r"expected|expand\w*|surge\w*|worth|revenue)\b",
    re.I,
)

# Report mills / press-release SEO aggregators: everything they publish under
# an industry query is a market-report announcement, headline pattern or not.
_MARKET_REPORT_SOURCES = {
    "exclusive press",
    "ein presswire",
    "openpr",
    "openpr.com",
    "imarc group",
    "mordor intelligence",
    "express press release distribution",
    "the business research company",
    "researchandmarkets.com",
    "globenewswire market research",
}


def _is_market_report(art: dict) -> bool:
    # Check the publisher name and the domain: providers that return no
    # publisher name would otherwise escape source-based detection entirely.
    if (art.get("published_by") or "").strip().lower() in _MARKET_REPORT_SOURCES:
        return True
    if article_domain(art) in _MARKET_REPORT_SOURCES:
        return True
    return bool(_MARKET_REPORT_RE.search(art.get("headline") or ""))


def _compute_dup_groups(articles: list[dict]) -> list[int]:
    """Assign a 1-based group id per article. Articles in the same group are
    duplicates: same canonical URL, or (failing that) same source+headline-stem.
    Returns a list parallel to ``articles``."""
    url_to_group: dict[str, int] = {}
    pair_to_group: dict[str, int] = {}
    groups: list[int] = []
    next_id = 1
    for art in articles:
        url_key = _normalise_url(art.get("document_url", ""))
        if url_key and url_key in url_to_group:
            groups.append(url_to_group[url_key])
            continue
        # Key on the headline stem alone. Keying on the publisher name (as this
        # used to) makes dup detection depend on whether a provider's API
        # returns one: providers that return nothing get a blank key that
        # collapses unrelated stories together, while those that do escape
        # cross-outlet syndication detection entirely. A matching 60-char stem
        # is the same story regardless of who carried it.
        stem_key = _headline_stem(art.get("headline", ""))
        if stem_key and stem_key in pair_to_group:
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
        if stem_key:
            pair_to_group[stem_key] = gid
    return groups


def _dup_count(groups: list[int]) -> int:
    """Number of duplicate articles (i.e. excess rows beyond one canonical per group)."""
    return len(groups) - len(set(groups))


# --- Spelling variants -----------------------------------------------------
# examples.py deliberately queries some entities under two spellings that differ
# only by an accent or punctuation ("Klöckner Pentaplast" / "Klockner
# Pentaplast"). Without this comparison the judge sees them as two unrelated
# entities and the robustness question — can a provider find the company when
# the caller types the name without the umlaut? — never reaches the report.

_VARIANT_STRIP_RE = re.compile(r"[^a-z0-9]+")

# Below this URL overlap, two spellings of one name are answered inconsistently
# enough to be worth flagging to the judge.
VARIANT_OVERLAP_FLAG = 0.5


def _variant_key(name: str) -> str:
    """Fold a queried name to accents-, case- and punctuation-insensitive form.
    Two queried names sharing a key are spellings of the same entity."""
    folded = unicodedata.normalize("NFKD", name or "").encode("ascii", "ignore").decode()
    return _VARIANT_STRIP_RE.sub("", folded.lower())


def _variant_groups(names: list[str]) -> list[list[str]]:
    """Group queried names that differ only by accent, case or punctuation.
    Singletons are dropped — a name with no variant has nothing to compare."""
    by_key: dict[str, list[str]] = defaultdict(list)
    for name in names:
        key = _variant_key(name)
        if key:
            by_key[key].append(name)
    return [sorted(group) for _, group in sorted(by_key.items()) if len(group) > 1]


def variant_consistency(
    data: dict[str, dict[str, list[dict]]]
) -> list[dict]:
    """For each spelling-variant group, per provider: how many articles came
    back for each spelling and how far the returned URL sets overlap.

    ``data`` is the label → item-name → articles mapping the formatters build.
    Returns [] when the run queried no variant pairs, so the whole feature costs
    nothing on a query set that has none.

    Limitation: the pair is discovered from the names present in the CSV, not
    from examples.py — re-analysing an old run must not be reinterpreted through
    today's query list. Error rows still carry their name, so an all-errors
    spelling stays visible; a spelling for which every provider returned zero
    results leaves no rows at all and the pair goes undetected.
    """
    all_names = sorted({name for items in data.values() for name in items})
    groups = _variant_groups(all_names)
    out: list[dict] = []
    for variants in groups:
        per_provider: dict[str, dict] = {}
        for label in sorted(data):
            url_sets = []
            counts = []
            for name in variants:
                real = [
                    a for a in data[label].get(name, [])
                    if a.get("headline") != "*** ERROR ***"
                ]
                counts.append(len(real))
                url_sets.append(
                    {u for u in (_normalise_url(a.get("document_url", "")) for a in real) if u}
                )
            union = set().union(*url_sets)
            shared = set.intersection(*url_sets) if url_sets else set()
            per_provider[label] = {
                "counts": counts,
                "shared": len(shared),
                "union": len(union),
                "overlap": (len(shared) / len(union)) if union else None,
                "answered": [n for n, c in zip(variants, counts) if c],
            }
        out.append({"variants": variants, "providers": per_provider})
    return out


def _variant_verdict(stats: dict, variants: list[str]) -> str:
    """One-phrase read on a provider's handling of one variant pair."""
    answered = stats["answered"]
    if not answered:
        return "no results for either spelling"
    if len(answered) < len(variants):
        return f"answers only \"{answered[0]}\" ⚠"
    overlap = stats["overlap"]
    if overlap is None:
        return "no URLs to compare"
    if overlap >= 0.99:
        return "identical results — spelling-insensitive"
    if overlap < VARIANT_OVERLAP_FLAG:
        return "largely different results for the two spellings ⚠"
    return "partially overlapping results"


def variant_block(groups: list[dict], kind: str) -> str:
    """Render the variant comparison for the prompt. Empty string when the run
    has no variant pairs."""
    if not groups:
        return ""
    lines = [
        f"\n{'=' * 60}",
        "SPELLING-VARIANT CONSISTENCY  (harness-computed — ground truth)",
        "=" * 60,
        f"These {kind.lower()} names were queried under two spellings that differ",
        "only by accent, case or punctuation — they are the same real entity.",
        "A robust provider returns the same articles for both. Overlap is the",
        "share of returned URLs common to both spellings.",
    ]
    for group in groups:
        variants = group["variants"]
        lines.append(f"\n  {' vs '.join(variants)}")
        for label, stats in group["providers"].items():
            counts = " vs ".join(str(c) for c in stats["counts"])
            overlap = (
                f"{100 * stats['overlap']:.0f}%" if stats["overlap"] is not None else "n/a"
            )
            lines.append(
                f"    PROVIDER {label}: {counts} articles  |  "
                f"{stats['shared']}/{stats['union']} URLs shared  |  overlap {overlap}"
                f"  |  {_variant_verdict(stats, variants)}"
            )
    return "\n".join(lines) + "\n"


def variant_table_md(groups: list[dict], label_to_provider: dict) -> str:
    """Markdown table of the same comparison, appended to the saved .md with
    providers decoded. Written by the harness so the finding reaches the report
    whether or not the model chose to cite it."""
    if not groups:
        return ""
    lines = [
        "## Spelling-variant consistency (harness — authoritative)",
        "",
        "Entities queried under two spellings that differ only by accent, case or",
        "punctuation. Overlap is the share of returned URLs common to both.",
    ]
    for group in groups:
        variants = group["variants"]
        lines += [
            "",
            f"**{' vs '.join(variants)}**",
            "",
            "| Provider | " + " | ".join(f"articles for “{v}”" for v in variants)
            + " | shared URLs | overlap | read |",
            "|---|" + "---|" * (len(variants) + 3),
        ]
        for label, stats in group["providers"].items():
            counts = " | ".join(str(c) for c in stats["counts"])
            overlap = (
                f"{100 * stats['overlap']:.0f}%" if stats["overlap"] is not None else "—"
            )
            provider = label_to_provider.get(label, label)
            lines.append(
                f"| {provider} | {counts} | {stats['shared']}/{stats['union']} "
                f"| {overlap} | {_variant_verdict(stats, variants)} |"
            )
    return "\n".join(lines) + "\n"


# --- Provider self-reported relevance --------------------------------------
# Some providers return a relevance score with each result. This section reports
# what they said about their own answers. It NEVER filters on that score, and
# nothing downstream may start doing so: a provider that returns 79 results it
# scored below 0.12 has made a precision error, and silently dropping those rows
# would launder exactly the defect this benchmark exists to detect — the same
# reasoning that keeps perplexity_agent_client.py off the `search_results`
# blocks. The score is evidence, not a filter.

# Empirically derived from a 12-company probe of Tavily (2026-08-19): of 414
# results scoring below 0.1 not one was on-target, the 0.1–0.2 band was 7%
# on-target, and above 0.3 it was ~72%. Scores are not calibrated between
# providers, so this is a reading aid, not a universal constant — the band
# distribution is reported alongside so the threshold is not the whole story.
WEAK_SCORE = 0.2

SCORE_BANDS = [(0.0, 0.1), (0.1, 0.2), (0.2, 0.3), (0.3, 0.5), (0.5, 1.01)]


def _score_of(art: dict) -> float | None:
    """Provider-supplied relevance score, or None where it supplied none."""
    raw = art.get("relevance_score")
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def score_diagnostics(data: dict[str, dict[str, list[dict]]]) -> dict[str, dict]:
    """Per provider: whether it returns a relevance score, how those scores are
    distributed, and — the part a caller cannot see from one query — how many
    items it answered at length while scoring everything it returned as weak.

    ``data`` is the label → item-name → articles mapping the formatters build.
    Providers that supply no score are reported as such rather than omitted:
    shipping no usable score is itself a difference between providers.
    """
    out: dict[str, dict] = {}
    for label in sorted(data):
        scores: list[float] = []
        total = 0
        weak_items: list[tuple[str, int, float]] = []
        for name, arts in data[label].items():
            real = [a for a in arts if a.get("headline") != "*** ERROR ***"]
            total += len(real)
            item_scores = [s for s in (_score_of(a) for a in real) if s is not None]
            scores.extend(item_scores)
            # The provider's own best result for this item. A low best score is
            # the provider saying it found nothing — while still returning rows.
            if item_scores and max(item_scores) < WEAK_SCORE:
                weak_items.append((name, len(real), max(item_scores)))
        bands = [
            sum(1 for s in scores if lo <= s < hi) for lo, hi in SCORE_BANDS
        ]
        out[label] = {
            "total": total,
            "scored": len(scores),
            "median": statistics.median(scores) if scores else None,
            "bands": bands,
            "weak": sum(1 for s in scores if s < WEAK_SCORE),
            "weak_items": sorted(weak_items, key=lambda x: -x[1]),
        }
    return out


def _score_verdict(stats: dict) -> str:
    """One-phrase read on a provider's self-reported scores."""
    if not stats["scored"]:
        return "returns no relevance score — caller cannot triage its results"
    weak_pct = 100 * stats["weak"] / stats["scored"]
    n_weak_items = len(stats["weak_items"])
    if not n_weak_items and weak_pct < 25:
        return "scores its own results as mostly strong"
    parts = [f"{weak_pct:.0f}% of its results scored below {WEAK_SCORE}"]
    if n_weak_items:
        rows = sum(n for _, n, _ in stats["weak_items"])
        parts.append(
            f"{n_weak_items} items answered with {rows} articles it scored "
            f"entirely below {WEAK_SCORE} ⚠"
        )
    return "; ".join(parts)


def _band_str(bands: list[int]) -> str:
    return "  ".join(
        f"{lo:.1f}-{min(hi, 1.0):.1f}: {n}" for (lo, hi), n in zip(SCORE_BANDS, bands)
    )


def score_block(diag: dict[str, dict], kind: str) -> str:
    """Render the self-reported-score diagnostic for the prompt. Empty string
    when no provider in the run returned any score at all."""
    if not any(v["scored"] for v in diag.values()):
        return ""
    lines = [
        f"\n{'=' * 60}",
        "PROVIDER SELF-REPORTED RELEVANCE  (harness-computed — ground truth)",
        "=" * 60,
        "What each provider said about the quality of its own results. These",
        "scores are NOT used to filter anything — every article the provider",
        "returned is shown above regardless of what it scored. A provider that",
        f"answers a {kind.lower()} with articles it itself scored below "
        f"{WEAK_SCORE} is returning results it knew were weak — a precision",
        "failure the article list alone does not reveal.",
        "Scores are not comparable between providers; compare a provider only",
        "against its own results.",
    ]
    for label, stats in diag.items():
        lines.append(f"\n  PROVIDER {label}: {_score_verdict(stats)}")
        if not stats["scored"]:
            continue
        lines.append(
            f"    scored {stats['scored']}/{stats['total']} articles  |  "
            f"median {stats['median']:.3f}  |  bands  {_band_str(stats['bands'])}"
        )
        for name, n, best in stats["weak_items"][:10]:
            lines.append(
                f"    - \"{name}\": returned {n} articles, best score only {best:.3f}"
            )
        if len(stats["weak_items"]) > 10:
            lines.append(f"    … {len(stats['weak_items']) - 10} more such items")
    return "\n".join(lines) + "\n"


def score_table_md(diag: dict[str, dict], label_to_provider: dict) -> str:
    """Markdown table of the same diagnostic, appended to the saved .md with
    providers decoded. Written by the harness so the finding reaches the report
    whether or not the model chose to cite it."""
    if not any(v["scored"] for v in diag.values()):
        return ""
    lines = [
        "## Provider self-reported relevance (harness — authoritative)",
        "",
        f"What each provider said about its own results. Never used to filter "
        f"them. \"Weak items\" are queries the provider answered while scoring "
        f"every article it returned below {WEAK_SCORE}.",
        "",
        "| Provider | scored | median | weak items | read |",
        "|---|---|---|---|---|",
    ]
    for label, stats in diag.items():
        provider = label_to_provider.get(label, label)
        median = f"{stats['median']:.3f}" if stats["median"] is not None else "—"
        lines.append(
            f"| {provider} | {stats['scored']}/{stats['total']} | {median} "
            f"| {len(stats['weak_items'])} | {_score_verdict(stats)} |"
        )
    return "\n".join(lines) + "\n"


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
1. Score every provider on every axis (precision, coverage, metadata_integrity,
   story_quality, trust). Use the full 0–10 range. A 7 across the board
   is a refusal to judge — if the data shows a 3, write 3. Refusing to
   differentiate is itself a failure mode.
2. Every axis score must be backed by concrete evidence as an array of short
   strings. Each evidence string must name a queried entity (company name, or
   industry+location) and quote a headline, source, or pattern. Generic claims
   like "many results were off-topic" without examples are malformed and will
   be rejected.
3. Pre-computed flags in the data are ground truth — use them directly:
     - `[NO DATE ⚠]`, `STALE>90d ⚠` and `NO PUBLISHER ⚠` drive
       metadata_integrity. Weight the two unequally:
         * `no-date` is the severe one. A date cannot be recovered from
           anywhere else in the row, and without it the consumer cannot tell
           whether a story is from this week or three years ago. A large
           `no-date: N (X%)` share alone holds this axis at or below 3.
         * `no-publisher` is real but lesser. Every article shows its domain in
           parentheses — `| NO PUBLISHER ⚠ (reuters.com)` — and a domain is
           usually enough to judge credibility, so the information is degraded
           rather than absent. Weight it at roughly half the severity of
           `no-date`. A large `no-publisher: N (X%)` share alone should not
           push this axis below about 5.
       Do not treat a named publisher as evidence of quality on its own; judge
       the outlet, whether it arrives as a name or a domain.
     - `[DUP of #N ⚠]` flags and the `dup: N` count in each provider header
       drive uniqueness.
     - `[MKT-REPORT ⚠]` flags and the `mkt-report: N` header count identify
       market-research-report landing pages / SEO announcements.
     - `[NO RESULTS RETURNED ⚠]` items and the `answered: X/Y` count in each
       provider header drive coverage.
     - `*** ERROR ***` rows and the `errors: N` header count drive trust.
     - The `PROVIDER SELF-REPORTED RELEVANCE` section, when present, reports
       what each provider said about the quality of its own results. Nothing was
       filtered on it. A provider that answered an item with many articles while
       scoring every one of them as weak returned results it knew were poor —
       score that as precision, and quote the item names and counts. A provider
       returning no score at all is a usability limitation worth stating, not a
       precision failure. Never compare raw scores between providers.
     - The `SPELLING-VARIANT CONSISTENCY` section, when present, pairs queried
       names that are the same real entity spelled two ways (accent, case or
       punctuation). Answering one spelling and not the other is a coverage
       failure. Clean results for one spelling and wrong-entity noise for the
       other is a precision failure. Quote the overlap percentages.
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
| coverage          | 0.20   | At least one real, relevant article for nearly every queried entity (`answered: X/Y` header is ground truth) | Multiple queried entities return no results at all      |
| metadata_integrity | 0.15  | 0 no-date, 0 stale, publisher named on nearly every row | Large no-date or stale share (severe); large no-publisher share (about half as severe) |
| story_quality     | 0.15   | Summaries let user decide without clicking              | Boilerplate, cookie banners, "subscribe to read"                |
| trust             | 0.15   | 0 errors, no suspicious URLs                            | Hallucinated URLs/facts; high error rate                        |

PROVIDER SELF-REPORTED RELEVANCE
If the data carries a `PROVIDER SELF-REPORTED RELEVANCE` section, an item a
provider answered with many articles while scoring every one of them as weak is
a `precision` failure of the clearest kind: it returned results it had already
judged poor, and the caller has no way to know that from the article list alone.
Returning no score at all is not a precision failure — note it under
`story_quality` as a usability limitation and move on. Never rank providers by
raw score; the scores are not calibrated against each other.

SPELLING-VARIANT PAIRS
If the data carries a `SPELLING-VARIANT CONSISTENCY` section, the two spellings
in each pair are one entity, not two. Treat a provider that answers only one of
them as having missed that entity for `coverage` — the caller cannot be relied
on to type the accent — and score `precision` on the worse of the two spellings.
A provider whose two spellings return the same URLs is robust; say so.

For each axis, output a 0–10 score and an `evidence` array of 1–4 short strings.
Each evidence string MUST name a queried entity (or industry+location) and quote
a specific headline, source, or counted pattern. Anonymous claims are malformed.

SCORING — COMPUTED BY THE HARNESS, NOT BY YOU
Your axis scores are the only scoring input. After you respond, the harness
computes, for each provider:
  weighted = 0.35·precision + 0.20·coverage + 0.15·metadata_integrity
           + 0.15·story_quality + 0.15·trust
  hard caps: metadata_integrity ≤ 3 → final ≤ 5.0; metadata_integrity ≤ 5 →
  final ≤ 7.0; trust ≤ 4 → final ≤ 4.0; precision ≤ 3 → final ≤ 5.0
  final = min(weighted, applicable caps); ranking = final descending, ties
  broken by precision then metadata_integrity.
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
        "metadata_integrity": {"score": 0, "evidence": ["..."]},
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

NOTE on market-report landing pages: flagged inline as `[MKT-REPORT ⚠]`; the
header `mkt-report: N` count is ground truth. For a company query they are
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

INTENT CLAUSES
Some topic headers carry an `(intent: …)` clause listing the sub-segments the
query meant. Judge relevance against that sense of the industry term. E.g. for
"Film | CN (intent: BOPP Film, BOPET, PE Film)", plastic/packaging film
coverage is on-topic and cinema coverage is FP-entity — even though "film"
could plausibly mean either without the intent clause.

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
- FP-stale / FP-no-date / FP-dup: see header counts (ground truth). A missing
  publisher is NOT a false positive — the article's domain is still shown.
- FP-halluc: suspicious URL patterns; invented facts.
- Errors: `*** ERROR ***` rows — header `errors: N` is ground truth.

NOTE on market-report landing pages: flagged inline as `[MKT-REPORT ⚠]`; the
header `mkt-report: N` count is ground truth. A small number (≤2 per topic)
provides useful state-of-market context — count those as on-topic (TP /
TP-thin). Beyond that, surplus copies are noise — count the excess as
FP-not-news, and treat a provider whose results are dominated by them as a
precision failure. Do not blanket-penalise.

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
  (e.g. "metadata cap" or "trust cap") and the underlying reason (e.g. "12
  no-date results", "fabricated Reuters URLs").
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
    index: int, art: dict, reference_date: datetime, markers: list[str] | None = None
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
    for marker in markers or []:
        label_parts.append(f"[{marker} ⚠]")
    label_parts.append(headline)
    domain = article_domain(art)
    domain_part = f" ({domain})" if domain else ""
    label_parts.append(
        f"| {source}{domain_part}" if source else f"| NO PUBLISHER ⚠{domain_part}"
    )
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


def _no_publisher_count(arts: list[dict]) -> int:
    return sum(1 for a in arts if classify_publisher(a) == "no_publisher")


def _group_summary(
    label: str,
    all_real: list[dict],
    total_errors: int,
    reference_date: datetime,
    total_dups: int,
    total_mkt: int,
    answered: int,
    universe: int,
    kind: str,
) -> list[str]:
    no_date, stale = _date_counts(all_real, reference_date)
    no_publisher = _no_publisher_count(all_real)
    total = len(all_real)

    def with_pct(n: int) -> str:
        return f"{n} ({100 * n / total:.0f}%)" if total else str(n)

    kind_plural = "companies" if kind == "Company" else "topics"
    return [
        f"\n{'=' * 60}",
        (
            f"PROVIDER {label}  |  answered: {answered}/{universe} {kind_plural}  "
            f"|  total articles: {total}  |  errors: {total_errors}  "
            f"|  no-date: {with_pct(no_date)}  |  stale (>{STALE_DAYS}d): {with_pct(stale)}  "
            f"|  no-publisher: {with_pct(no_publisher)}  "
            f"|  dup: {with_pct(total_dups)}  |  mkt-report: {with_pct(total_mkt)}"
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
    mkt: int,
) -> str:
    no_date, stale = _date_counts(real, reference_date)
    no_publisher = _no_publisher_count(real)
    parts = [f"{len(real)} articles"]
    if errors:
        parts.append(f"{len(errors)} errors")
    if no_date:
        parts.append(f"{no_date} no-date")
    if no_publisher:
        parts.append(f"{no_publisher} no-publisher")
    if stale:
        parts.append(f"{stale} stale")
    if dup:
        parts.append(f"{dup} dup")
    if mkt:
        parts.append(f"{mkt} mkt-report")
    return f"\n  {kind}: {name}  ({', '.join(parts)})"


def _render_item(
    kind: str,
    name: str,
    real: list[dict],
    errors: list,
    reference_date: datetime,
    max_articles: int,
) -> tuple[list[str], int, int]:
    """Render one item (company or topic) in the provider's own result order —
    that is what a real consumer sees, and re-sorting by recency would bias the
    shown sample toward date-clustered newswire spam.
    Returns (lines, dup_count, mkt_report_count) for this item."""
    groups = _compute_dup_groups(real)
    item_dup = _dup_count(groups)
    mkt_flags = [_is_market_report(a) for a in real]
    item_mkt = sum(mkt_flags)

    lines = [_item_header(kind, name, real, errors, reference_date, item_dup, item_mkt)]
    if not real:
        lines.append("    [NO RESULTS RETURNED ⚠]")
        return lines, item_dup, item_mkt

    shown = real[:max_articles]
    shown_groups = groups[: len(shown)]
    canonical_pos: dict[int, int] = {}
    for i, gid in enumerate(shown_groups, 1):
        canonical_pos.setdefault(gid, i)

    for i, (art, gid) in enumerate(zip(shown, shown_groups), 1):
        canon = canonical_pos[gid]
        markers = []
        if canon != i:
            markers.append(f"DUP of #{canon}")
        if mkt_flags[i - 1]:
            markers.append("MKT-REPORT")
        lines.extend(_format_article(i, art, reference_date, markers))

    if len(real) > max_articles:
        lines.append(f"    … {len(real) - max_articles} more articles not shown")

    return lines, item_dup, item_mkt


def group_rows(
    rows: list[dict], provider_to_label: dict, query_type: str
) -> dict[str, dict[str, list[dict]]]:
    """Group raw CSV rows as label → item name → articles. Shared by the prompt
    formatters and the harness-computed variant table so both see one grouping."""
    data: dict[str, dict[str, list[dict]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label = provider_to_label.get(row.get("provider", ""), row.get("provider", ""))
        if query_type == "companies":
            name = row.get("company", "")
        else:
            name = f"{row.get('industry', '')} | {row.get('location', '')}"
            # Surface the query's intended sense of the industry term (e.g.
            # "Film" meaning plastic film, not cinema) so the judge scores
            # against it.
            context = (row.get("industry_context") or "").strip()
            if context:
                name = f"{name} (intent: {context})"
        data[label][name].append(row)
    return data


def format_companies_data(
    rows: list[dict], provider_to_label: dict, max_articles: int, reference_date: datetime
) -> str:
    data = group_rows(rows, provider_to_label, "companies")
    return _format_grouped("Company", data, reference_date, max_articles)


def format_industries_data(
    rows: list[dict], provider_to_label: dict, max_articles: int, reference_date: datetime
) -> str:
    data = group_rows(rows, provider_to_label, "industries")
    return _format_grouped("Topic", data, reference_date, max_articles)


def _format_grouped(
    kind: str,
    data: dict[str, dict[str, list[dict]]],
    reference_date: datetime,
    max_articles: int,
) -> str:
    # Universe of queried items across all providers. A provider with no rows
    # for an item returned nothing for it — that gap must be rendered, or the
    # judge cannot see (and has previously hallucinated) coverage.
    all_names = sorted({name for items in data.values() for name in items})

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

        # First render each item to get per-item dup/mkt counts; then prepend
        # the provider header with the aggregate totals.
        item_blocks: list[list[str]] = []
        total_dups = 0
        total_mkt = 0
        answered = 0
        for name in all_names:
            all_arts = items.get(name, [])
            errors = [a for a in all_arts if a.get("headline") == "*** ERROR ***"]
            real = [a for a in all_arts if a.get("headline") != "*** ERROR ***"]
            if real:
                answered += 1
            block, item_dup, item_mkt = _render_item(
                kind, name, real, errors, reference_date, max_articles
            )
            total_dups += item_dup
            total_mkt += item_mkt
            item_blocks.append(block)

        lines.extend(
            _group_summary(
                label, all_real, total_errors, reference_date,
                total_dups, total_mkt, answered, len(all_names), kind,
            )
        )
        for block in item_blocks:
            lines.extend(block)

    # Spelling-variant pairs are queried as separate items, so the per-item
    # blocks above cannot show that two of them are the same entity. Append the
    # cross-item comparison so the judge can score robustness to spelling.
    lines.append(variant_block(variant_consistency(data), kind))
    # Providers that return a relevance score have told us what they made of
    # their own answers. Reported, never acted on — see score_diagnostics.
    lines.append(score_block(score_diagnostics(data), kind))

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
            # claude-opus-4-7 rejects the temperature param as deprecated, so
            # run-to-run judging variance cannot be pinned down that way.
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
    meta = axes["metadata_integrity"]["score"]
    trust = axes["trust"]["score"]
    prec = axes["precision"]["score"]
    if meta <= CAP_METADATA_HARD_THRESHOLD:
        caps.append("metadata_hard")
        final = min(final, CAP_METADATA_HARD_LIMIT)
    elif meta <= CAP_METADATA_SOFT_THRESHOLD:
        caps.append("metadata_soft")
        final = min(final, CAP_METADATA_SOFT_LIMIT)
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
            -p["axes"]["metadata_integrity"]["score"],
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


def scorecard_table_md(scorecard: dict) -> str:
    """Markdown table of the harness-recomputed scores, appended to the saved
    .md so a human reader never trusts model-authored arithmetic that may
    survive in the raw output above it."""
    lines = [
        "## Recomputed scorecard (harness — authoritative)",
        "",
        "Axis scores are the model's; `weighted`, `final`, caps and the ranking",
        "are recomputed by the harness. If numbers in the raw output above",
        "disagree, this table wins.",
        "",
        "| Rank | Provider | " + " | ".join(RUBRIC_AXES) + " | weighted | final | caps |",
        "|---|---|" + "---|" * (len(RUBRIC_AXES) + 3),
    ]
    for rank, prov in enumerate(scorecard["providers"], 1):
        axes = prov["axes"]
        scores = " | ".join(str(axes[a]["score"]) for a in RUBRIC_AXES)
        caps = ", ".join(prov.get("caps_applied", [])) or "—"
        lines.append(
            f"| {rank} | {prov['label']} | {scores} "
            f"| {prov['weighted']} | {prov['final']} | {caps} |"
        )
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Evidence verification
# ---------------------------------------------------------------------------

def build_evidence_index(
    rows: list[dict], provider_to_label: dict, query_type: str
) -> tuple[dict[str, set], dict[str, set]]:
    """Build (alias→entity-keys, label→answered-entity-keys) from the raw rows.

    Aliases are lowercase strings the model plausibly uses to name a queried
    entity in evidence ("BOPET/CN", "BOARD | Eastern Asia", a company name).
    """
    alias_map: dict[str, set] = defaultdict(set)
    answered: dict[str, set] = defaultdict(set)
    variant_aliases: dict[str, set] = defaultdict(set)
    if query_type == "companies":
        for row in rows:
            name = (row.get("company") or "").strip()
            if name:
                variant_aliases[_variant_key(name)].add(name.lower())
    for row in rows:
        if row.get("headline") == "*** ERROR ***":
            continue
        label = provider_to_label.get(row.get("provider", ""), row.get("provider", ""))
        if query_type == "companies":
            name = (row.get("company") or "").strip()
            if not name:
                continue
            key = name.lower()
            # Very short names substring-match too freely to be useful.
            aliases = {key} if len(key) >= 4 else set()
            # A spelling-variant pair is one entity: evidence naming either
            # spelling is legitimate if the provider answered either, so map
            # every variant's alias onto this key as well.
            for other in variant_aliases.get(_variant_key(name), ()):  # noqa: B023
                if len(other) >= 4:
                    aliases.add(other)
        else:
            industry = (row.get("industry") or "").strip()
            location = (row.get("location") or "").strip()
            key = f"{industry}|{location}".lower()
            aliases = set()
            if location:
                for sep in ("/", " | ", "|", ", "):
                    aliases.add(f"{industry}{sep}{location}".lower())
            elif len(industry) >= 4:
                aliases.add(industry.lower())
        answered[label].add(key)
        for alias in aliases:
            alias_map[alias].add(key)
    return alias_map, answered


# Evidence that legitimately names an entity as EMPTY or FAILED must not be
# flagged as a hallucination — only positive claims about absent data are.
_NEGATIVE_EVIDENCE_RE = re.compile(
    r"zero|no results|no articles|0 articles|returned no|empty|error|answered \d+/\d+",
    re.I,
)


def verify_evidence(
    scorecard: dict, alias_map: dict[str, set], answered: dict[str, set]
) -> int:
    """Warn when an evidence string cites a queried entity the provider has no
    results for — the tell-tale of a hallucinated example. Returns warning count."""
    warnings = 0
    for prov in scorecard.get("providers", []):
        label = prov.get("label", "?")
        have = answered.get(label, set())
        for axis, ax in prov.get("axes", {}).items():
            for ev in ax.get("evidence", []):
                if _NEGATIVE_EVIDENCE_RE.search(ev):
                    continue
                ev_lower = ev.lower()
                for alias, keys in alias_map.items():
                    if alias in ev_lower and not (keys & have):
                        warnings += 1
                        print(
                            f"  ⚠ Evidence check: provider {label} / {axis} cites "
                            f"'{alias}' but has no results for it: \"{ev[:90]}\""
                        )
    return warnings


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

    companies_variants = variant_consistency(
        group_rows(companies_rows, provider_to_label, "companies")
    )
    industries_variants = variant_consistency(
        group_rows(industries_rows, provider_to_label, "industries")
    )
    print(
        "Spelling-variant pairs found: "
        f"{len(companies_variants)} companies, {len(industries_variants)} topics"
    )

    companies_scores = score_diagnostics(
        group_rows(companies_rows, provider_to_label, "companies")
    )
    industries_scores = score_diagnostics(
        group_rows(industries_rows, provider_to_label, "industries")
    )
    scored_providers = sum(1 for v in companies_scores.values() if v["scored"])
    print(
        f"Providers returning a relevance score: {scored_providers}"
        f"/{len(companies_scores)}"
    )

    print("Verifying evidence strings against the data…")
    alias_map, answered = build_evidence_index(companies_rows, provider_to_label, "companies")
    n_warn = verify_evidence(companies_scorecard, alias_map, answered)
    alias_map, answered = build_evidence_index(industries_rows, provider_to_label, "industries")
    n_warn += verify_evidence(industries_scorecard, alias_map, answered)
    print(f"  Evidence check complete: {n_warn} warning(s).")

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
        f.write("\n\n---\n\n")
        f.write(scorecard_table_md(companies_scorecard))
        if companies_variants:
            f.write("\n---\n\n")
            f.write(variant_table_md(companies_variants, label_to_provider))
        score_md = score_table_md(companies_scores, label_to_provider)
        if score_md:
            f.write("\n---\n\n")
            f.write(score_md)

    industries_path = os.path.join(ai_dir, f"claude-industries-{timestamp}.md")
    with open(industries_path, "w") as f:
        f.write(f"# Industries Analysis — {timestamp}\n\n")
        f.write(f"*Model: {model} | Max articles per topic per provider: {max_articles}*\n\n")
        f.write(f"*Provider labels were anonymised. See `decode-key-{timestamp}.json` to decode.*\n\n")
        f.write("---\n\n")
        f.write(industries_analysis)
        f.write("\n\n---\n\n")
        f.write(scorecard_table_md(industries_scorecard))
        if industries_variants:
            f.write("\n---\n\n")
            f.write(variant_table_md(industries_variants, label_to_provider))
        score_md = score_table_md(industries_scores, label_to_provider)
        if score_md:
            f.write("\n---\n\n")
            f.write(score_md)

    # Keep the comparison in the machine-readable scorecards too, so a later run
    # can diff spelling robustness without re-parsing the markdown.
    companies_scorecard["spelling_variants"] = companies_variants
    industries_scorecard["spelling_variants"] = industries_variants
    companies_scorecard["self_reported_scores"] = companies_scores
    industries_scorecard["self_reported_scores"] = industries_scores

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
