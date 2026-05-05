"""Tests for analyse.py — pure-Python, no API calls."""

import json
from datetime import datetime, timezone

import pytest

from analyse import (
    CAP_PRECISION_LIMIT,
    CAP_PRECISION_THRESHOLD,
    CAP_RECENCY_HARD_LIMIT,
    CAP_RECENCY_HARD_THRESHOLD,
    CAP_RECENCY_SOFT_LIMIT,
    CAP_RECENCY_SOFT_THRESHOLD,
    CAP_TRUST_LIMIT,
    CAP_TRUST_THRESHOLD,
    STALE_DAYS,
    _apply_caps,
    _compute_dup_groups,
    _dup_count,
    _format_article,
    _headline_stem,
    _normalise_url,
    _recompute_provider,
    _render_item,
    classify_date,
    format_companies_data,
    make_anonymization,
    parse_scorecard,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REF = datetime(2026, 4, 20, tzinfo=timezone.utc)


def _prov(precision=8, recency=9, recall=7, uniqueness=8, summary=7, trust=9, label="A"):
    """Minimal valid provider dict for testing."""
    return {
        "label": label,
        "axes": {
            "precision":         {"score": precision, "evidence": ["x"]},
            "recency_integrity": {"score": recency,   "evidence": ["x"]},
            "recall":            {"score": recall,     "evidence": ["x"]},
            "uniqueness":        {"score": uniqueness, "evidence": ["x"]},
            "summary":           {"score": summary,    "evidence": ["x"]},
            "trust":             {"score": trust,      "evidence": ["x"]},
        },
        "weighted": 0.0,
        "caps_applied": [],
        "final": 0.0,
        "verdict": "ok",
    }


def _scorecard_text(providers: list[dict], query_type: str = "companies", notes: str = "") -> str:
    """Wrap providers in a valid fenced-JSON analysis blob."""
    ranking = [p["label"] for p in providers]
    data = {
        "query_type": query_type,
        "providers": providers,
        "ranking": ranking,
        "ranking_rationale": {
            f"{i+1}{'st' if i==0 else 'nd' if i==1 else 'rd' if i==2 else 'th'}": "reason"
            for i in range(len(providers))
        },
    }
    body = f"```json\n{json.dumps(data, indent=2)}\n```"
    if notes:
        body += f"\n\n## Notes\n\n{notes}"
    return body


# ---------------------------------------------------------------------------
# _normalise_url
# ---------------------------------------------------------------------------

class TestNormaliseUrl:
    def test_strips_utm(self):
        url = "https://www.example.com/a?utm_source=x&utm_medium=y&q=1"
        norm = _normalise_url(url)
        assert "utm_source" not in norm
        assert "utm_medium" not in norm
        assert "q=1" in norm

    def test_strips_www(self):
        assert _normalise_url("https://www.example.com/a") == _normalise_url("https://example.com/a")

    def test_strips_trailing_slash(self):
        assert _normalise_url("https://example.com/a/") == _normalise_url("https://example.com/a")

    def test_lowercases_scheme_and_host(self):
        assert _normalise_url("HTTPS://Example.COM/path") == _normalise_url("https://example.com/path")

    def test_drops_fragment(self):
        norm = _normalise_url("https://example.com/a#section")
        assert "#" not in norm


# ---------------------------------------------------------------------------
# _headline_stem
# ---------------------------------------------------------------------------

class TestHeadlineStem:
    def test_lowercases(self):
        assert _headline_stem("ACME Acquires Beta") == _headline_stem("acme acquires beta")

    def test_strips_punctuation(self):
        assert "!" not in _headline_stem("Acme buys Beta!")

    def test_truncates_at_60(self):
        long = "a" * 100
        assert len(_headline_stem(long)) == 60


# ---------------------------------------------------------------------------
# _compute_dup_groups / _dup_count
# ---------------------------------------------------------------------------

class TestDupGroups:
    def _make(self, url="", source="", headline=""):
        return {"document_url": url, "published_by": source, "headline": headline}

    def test_same_url_is_dup(self):
        arts = [
            self._make(url="https://example.com/a"),
            self._make(url="https://example.com/a"),
            self._make(url="https://example.com/b"),
        ]
        groups = _compute_dup_groups(arts)
        assert groups[0] == groups[1]
        assert groups[2] != groups[0]
        assert _dup_count(groups) == 1

    def test_same_headline_stem_same_source_is_dup(self):
        # Stem matching is exact after lowercasing + stripping non-alphanumerics.
        # Same source + same stem → dup; different source → NOT a dup.
        arts = [
            self._make(url="https://a.com/x", source="Reuters", headline="Acme buys Beta!!!"),
            self._make(url="https://b.com/y", source="Reuters", headline="Acme BUYS Beta..."),
            self._make(url="https://c.com/z", source="Bloomberg", headline="Acme buys Beta!!!"),
        ]
        groups = _compute_dup_groups(arts)
        assert groups[0] == groups[1]
        assert groups[2] != groups[0]
        assert _dup_count(groups) == 1

    def test_normalised_url_matches(self):
        arts = [
            self._make(url="https://www.example.com/a?utm_source=x"),
            self._make(url="https://example.com/a/"),
        ]
        groups = _compute_dup_groups(arts)
        assert groups[0] == groups[1]


# ---------------------------------------------------------------------------
# classify_date
# ---------------------------------------------------------------------------

class TestClassifyDate:
    def test_recent(self):
        art = {"published_date_clean": REF.isoformat()}
        assert classify_date(art, REF) == "recent"

    def test_stale(self):
        stale_dt = REF.replace(year=REF.year - 1)
        art = {"published_date_clean": stale_dt.isoformat()}
        assert classify_date(art, REF) == "stale"

    def test_no_date(self):
        assert classify_date({}, REF) == "no_date"

    def test_exactly_at_stale_boundary(self):
        from datetime import timedelta
        just_over = REF - timedelta(days=STALE_DAYS + 1)
        art = {"published_date_clean": just_over.isoformat()}
        assert classify_date(art, REF) == "stale"

    def test_naive_datetime_treated_as_utc(self):
        naive_iso = "2026-04-19T12:00:00"   # no tz
        art = {"published_date_clean": naive_iso}
        assert classify_date(art, REF) == "recent"


# ---------------------------------------------------------------------------
# _apply_caps
# ---------------------------------------------------------------------------

class TestApplyCaps:
    def _axes(self, prec=8, rec=9, trust=9):
        return {
            "precision":         {"score": prec},
            "recency_integrity": {"score": rec},
            "trust":             {"score": trust},
        }

    def test_no_caps(self):
        final, caps = _apply_caps(self._axes(), weighted=7.5)
        assert final == 7.5
        assert caps == []

    def test_recency_hard_cap(self):
        final, caps = _apply_caps(self._axes(rec=CAP_RECENCY_HARD_THRESHOLD), weighted=8.0)
        assert "recency_hard" in caps
        assert final <= CAP_RECENCY_HARD_LIMIT

    def test_recency_soft_cap(self):
        final, caps = _apply_caps(self._axes(rec=CAP_RECENCY_SOFT_THRESHOLD), weighted=8.0)
        assert "recency_soft" in caps
        assert final <= CAP_RECENCY_SOFT_LIMIT

    def test_recency_between_thresholds(self):
        # rec just above hard threshold → only soft cap
        rec = CAP_RECENCY_HARD_THRESHOLD + 1
        assert rec <= CAP_RECENCY_SOFT_THRESHOLD
        final, caps = _apply_caps(self._axes(rec=rec), weighted=8.0)
        assert "recency_soft" in caps
        assert "recency_hard" not in caps

    def test_trust_cap(self):
        final, caps = _apply_caps(self._axes(trust=CAP_TRUST_THRESHOLD), weighted=8.0)
        assert "trust" in caps
        assert final <= CAP_TRUST_LIMIT

    def test_precision_cap(self):
        final, caps = _apply_caps(self._axes(prec=CAP_PRECISION_THRESHOLD), weighted=8.0)
        assert "precision" in caps
        assert final <= CAP_PRECISION_LIMIT

    def test_multiple_caps_take_minimum(self):
        final, caps = _apply_caps(
            self._axes(rec=CAP_RECENCY_HARD_THRESHOLD, trust=CAP_TRUST_THRESHOLD),
            weighted=8.0,
        )
        assert "recency_hard" in caps
        assert "trust" in caps
        assert final <= min(CAP_RECENCY_HARD_LIMIT, CAP_TRUST_LIMIT)

    def test_no_cap_when_just_above_threshold(self):
        _, caps = _apply_caps(self._axes(rec=CAP_RECENCY_SOFT_THRESHOLD + 1), weighted=7.0)
        assert "recency_soft" not in caps
        assert "recency_hard" not in caps


# ---------------------------------------------------------------------------
# _recompute_provider
# ---------------------------------------------------------------------------

class TestRecomputeProvider:
    def test_correct_weighted_calculation(self):
        # precision=10, all others=0 → weighted = 0.30*10 = 3.0
        p = _prov(precision=10, recency=0, recall=0, uniqueness=0, summary=0, trust=0)
        _recompute_provider(p)
        assert abs(p["weighted"] - 3.0) < 0.01

    def test_all_tens_gives_10(self):
        p = _prov(10, 10, 10, 10, 10, 10)
        _recompute_provider(p)
        assert p["weighted"] == 10.0
        assert p["final"] == 10.0

    def test_raises_on_missing_axis(self):
        p = _prov()
        del p["axes"]["precision"]
        with pytest.raises(ValueError, match="missing axes"):
            _recompute_provider(p)

    def test_caps_applied_set_correctly(self):
        p = _prov(recency=1)
        _recompute_provider(p)
        assert "recency_hard" in p["caps_applied"]


# ---------------------------------------------------------------------------
# parse_scorecard
# ---------------------------------------------------------------------------

class TestParseScorecard:
    def _two_provider_text(self):
        providers = [_prov(label="A"), _prov(precision=2, label="B")]
        for p in providers:
            p["weighted"] = 7.0
            p["final"] = 7.0
        return _scorecard_text(providers)

    def test_extracts_providers(self):
        result = parse_scorecard(self._two_provider_text())
        assert len(result["providers"]) == 2

    def test_ranking_derived_from_final(self):
        # A has precision=8 (higher), B has precision=2 (lower → precision cap)
        result = parse_scorecard(self._two_provider_text())
        assert result["ranking"][0] == "A"
        assert result["ranking"][1] == "B"

    def test_recomputes_scores(self):
        providers = [_prov(label="A")]
        providers[0]["weighted"] = 99.0  # wrong — should be recomputed
        providers[0]["final"] = 99.0
        result = parse_scorecard(_scorecard_text(providers))
        assert result["providers"][0]["weighted"] != 99.0
        assert result["providers"][0]["final"] != 99.0

    def test_raises_on_no_json_block(self):
        with pytest.raises(ValueError, match="No.*json"):
            parse_scorecard("Just some prose, no fenced block.")

    def test_raises_on_invalid_score(self):
        providers = [_prov(label="A")]
        providers[0]["axes"]["precision"]["score"] = 11  # out of range
        with pytest.raises(ValueError, match="invalid score"):
            parse_scorecard(_scorecard_text(providers))

    def test_raises_on_missing_providers_key(self):
        text = '```json\n{"query_type": "companies"}\n```'
        with pytest.raises(ValueError, match="missing 'providers'"):
            parse_scorecard(text)


# ---------------------------------------------------------------------------
# _format_article
# ---------------------------------------------------------------------------

class TestFormatArticle:
    def _art(self, date="2026-04-10T00:00:00+00:00", headline="Acme Q1 results", source="Reuters",
             url="https://reuters.com/x", summary="Acme reported strong earnings."):
        return {
            "published_date_clean": date,
            "headline": headline,
            "published_by": source,
            "document_url": url,
            "summary_text": summary,
        }

    def test_no_date_flag(self):
        art = self._art(date="")
        lines = _format_article(1, art, REF)
        assert any("NO DATE" in l for l in lines)

    def test_stale_flag(self):
        art = self._art(date="2020-01-01T00:00:00+00:00")
        lines = _format_article(1, art, REF)
        assert any("STALE" in l for l in lines)

    def test_dup_marker_shown(self):
        lines = _format_article(2, self._art(), REF, dup_marker="DUP of #1")
        assert "DUP of #1" in lines[0]

    def test_summary_truncated(self):
        long_summary = "x" * 300
        art = self._art(summary=long_summary)
        lines = _format_article(1, art, REF)
        summary_line = next(l for l in lines if "x" in l)
        assert len(summary_line) < 300

    def test_no_url_line_when_empty(self):
        art = self._art(url="")
        lines = _format_article(1, art, REF)
        assert not any("URL:" in l for l in lines)


# ---------------------------------------------------------------------------
# _render_item
# ---------------------------------------------------------------------------

class TestRenderItem:
    def _make_articles(self, n=3, base_date="2026-04-10"):
        return [
            {
                "published_date_clean": f"{base_date}T{i:02d}:00:00+00:00",
                "headline": f"Headline {i}",
                "published_by": "Reuters",
                "document_url": f"https://reuters.com/{i}",
                "summary_text": f"Summary {i}.",
            }
            for i in range(n)
        ]

    def test_respects_max_articles(self):
        arts = self._make_articles(10)
        lines, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=3)
        shown = [l for l in lines if l.strip().startswith(tuple("0123456789"))]
        assert len(shown) <= 3
        assert any("more articles not shown" in l for l in lines)

    def test_counts_dups(self):
        arts = self._make_articles(2)
        arts[1]["document_url"] = arts[0]["document_url"]  # force dup
        _, dup_count = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert dup_count == 1

    def test_no_articles(self):
        lines, dup_count = _render_item("Company", "Acme", [], [], REF, max_articles=15)
        assert any("No articles" in l for l in lines)
        assert dup_count == 0


# ---------------------------------------------------------------------------
# format_companies_data
# ---------------------------------------------------------------------------

class TestFormatCompaniesData:
    def test_dup_in_header(self):
        rows = [
            {
                "provider": "Exa", "company": "Acme",
                "headline": "Acme acquires Beta", "published_by": "Reuters",
                "published_date_clean": "2026-04-10T00:00:00+00:00",
                "published_date": "", "document_url": "https://reuters.com/1",
                "summary_text": "", "industry": "", "location": "", "activity_type": "",
            },
            {
                "provider": "Exa", "company": "Acme",
                "headline": "Acme acquires Beta", "published_by": "Reuters",
                "published_date_clean": "2026-04-09T00:00:00+00:00",
                "published_date": "", "document_url": "https://reuters.com/1",  # same URL
                "summary_text": "", "industry": "", "location": "", "activity_type": "",
            },
        ]
        _, p2l = make_anonymization(["Exa"])
        out = format_companies_data(rows, p2l, max_articles=15, reference_date=REF)
        assert "dup: 1" in out


# ---------------------------------------------------------------------------
# make_anonymization
# ---------------------------------------------------------------------------

class TestMakeAnonymization:
    def test_roundtrip(self):
        providers = ["Exa", "Linkup", "Perplexity", "Syracuse", "Tavily"]
        l2p, p2l = make_anonymization(providers)
        assert set(l2p.values()) == set(providers)
        assert set(l2p.keys()) == set("ABCDE")
        for label, provider in l2p.items():
            assert p2l[provider] == label

    def test_randomised_each_call(self):
        providers = ["Exa", "Linkup", "Perplexity", "Syracuse", "Tavily"]
        mappings = [make_anonymization(providers)[0] for _ in range(20)]
        # After 20 shuffles, at least two should differ (probability of all identical ≈ 0)
        unique = {tuple(sorted(m.items())) for m in mappings}
        assert len(unique) > 1
