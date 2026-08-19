"""Tests for analyse.py — pure-Python, no API calls."""

import json
from datetime import datetime, timezone

import pytest

from analyse import (
    CAP_PRECISION_LIMIT,
    CAP_PRECISION_THRESHOLD,
    CAP_METADATA_HARD_LIMIT,
    CAP_METADATA_HARD_THRESHOLD,
    CAP_METADATA_SOFT_LIMIT,
    CAP_METADATA_SOFT_THRESHOLD,
    CAP_TRUST_LIMIT,
    CAP_TRUST_THRESHOLD,
    STALE_DAYS,
    _apply_caps,
    _compute_dup_groups,
    _dup_count,
    _format_article,
    _headline_sentence,
    _headline_stem,
    _normalise_url,
    _recompute_provider,
    _render_item,
    WEAK_SCORE,
    _score_of,
    _variant_groups,
    _variant_key,
    build_evidence_index,
    classify_date,
    classify_publisher,
    format_companies_data,
    group_rows,
    make_anonymization,
    parse_scorecard,
    score_block,
    score_diagnostics,
    score_table_md,
    variant_block,
    variant_consistency,
    variant_table_md,
    verify_evidence,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

REF = datetime(2026, 4, 20, tzinfo=timezone.utc)


def _prov(precision=8, coverage=7, recency=9, story_quality=7, trust=9, label="A"):
    """Minimal valid provider dict for testing (matches the current 5-axis rubric).

    Positional order matches RUBRIC_AXES: precision, coverage, metadata_integrity,
    story_quality, trust. Does not include weighted/final/caps_applied — the
    model no longer emits those; parse_scorecard/_recompute_provider compute
    them from the axis scores.
    """
    return {
        "label": label,
        "axes": {
            "precision":         {"score": precision,      "evidence": ["x"]},
            "coverage":          {"score": coverage,        "evidence": ["x"]},
            "metadata_integrity": {"score": recency,         "evidence": ["x"]},
            "story_quality":     {"score": story_quality,   "evidence": ["x"]},
            "trust":             {"score": trust,           "evidence": ["x"]},
        },
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

    def test_same_headline_stem_is_dup_across_outlets(self):
        # Stem matching is exact after lowercasing + stripping non-alphanumerics.
        # The same story syndicated to three outlets is two duplicates — the
        # publisher name is deliberately not part of the key, so providers that
        # return one are not judged differently from providers that do not.
        arts = [
            self._make(url="https://a.com/x", source="Reuters", headline="Acme buys Beta!!!"),
            self._make(url="https://b.com/y", source="Reuters", headline="Acme BUYS Beta..."),
            self._make(url="https://c.com/z", source="", headline="Acme buys Beta!!!"),
        ]
        groups = _compute_dup_groups(arts)
        assert groups[0] == groups[1] == groups[2]
        assert _dup_count(groups) == 2

    def test_different_headlines_not_dup_when_publisher_blank(self):
        # Blank publisher must not collapse unrelated stories together.
        arts = [
            self._make(url="https://a.com/x", source="", headline="Acme buys Beta"),
            self._make(url="https://b.com/y", source="", headline="Gamma opens plant"),
        ]
        assert _dup_count(_compute_dup_groups(arts)) == 0

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
            "metadata_integrity": {"score": rec},
            "trust":             {"score": trust},
        }

    def test_no_caps(self):
        final, caps = _apply_caps(self._axes(), weighted=7.5)
        assert final == 7.5
        assert caps == []

    def test_metadata_hard_cap(self):
        final, caps = _apply_caps(self._axes(rec=CAP_METADATA_HARD_THRESHOLD), weighted=8.0)
        assert "metadata_hard" in caps
        assert final <= CAP_METADATA_HARD_LIMIT

    def test_metadata_soft_cap(self):
        final, caps = _apply_caps(self._axes(rec=CAP_METADATA_SOFT_THRESHOLD), weighted=8.0)
        assert "metadata_soft" in caps
        assert final <= CAP_METADATA_SOFT_LIMIT

    def test_metadata_between_thresholds(self):
        # rec just above hard threshold → only soft cap
        rec = CAP_METADATA_HARD_THRESHOLD + 1
        assert rec <= CAP_METADATA_SOFT_THRESHOLD
        final, caps = _apply_caps(self._axes(rec=rec), weighted=8.0)
        assert "metadata_soft" in caps
        assert "metadata_hard" not in caps

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
            self._axes(rec=CAP_METADATA_HARD_THRESHOLD, trust=CAP_TRUST_THRESHOLD),
            weighted=8.0,
        )
        assert "metadata_hard" in caps
        assert "trust" in caps
        assert final <= min(CAP_METADATA_HARD_LIMIT, CAP_TRUST_LIMIT)

    def test_no_cap_when_just_above_threshold(self):
        _, caps = _apply_caps(self._axes(rec=CAP_METADATA_SOFT_THRESHOLD + 1), weighted=7.0)
        assert "metadata_soft" not in caps
        assert "metadata_hard" not in caps


# ---------------------------------------------------------------------------
# _recompute_provider
# ---------------------------------------------------------------------------

class TestRecomputeProvider:
    def test_correct_weighted_calculation(self):
        # precision=10, all others=0 → weighted = 0.35*10 = 3.5
        p = _prov(precision=10, coverage=0, recency=0, story_quality=0, trust=0)
        _recompute_provider(p)
        assert abs(p["weighted"] - 3.5) < 0.01

    def test_all_tens_gives_10(self):
        p = _prov(10, 10, 10, 10, 10)
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
        assert "metadata_hard" in p["caps_applied"]


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

    def test_strips_ranking_rationale(self):
        # A model-authored ranking_rationale reflects the model's own
        # (unreliable) arithmetic and can contradict the recomputed ranking —
        # parse_scorecard must discard it even if the model still emits one.
        providers = [_prov(label="A"), _prov(precision=2, label="B")]
        result = parse_scorecard(_scorecard_text(providers))
        assert "ranking_rationale" not in result


# ---------------------------------------------------------------------------
# _headline_sentence
# ---------------------------------------------------------------------------

class TestHeadlineSentence:
    def test_same_winner_both_query_types(self):
        companies = {"ranking": ["A", "B"]}
        industries = {"ranking": ["A", "C"]}
        label_to_provider = {"A": "Syracuse", "B": "Perplexity", "C": "Exa"}
        result = _headline_sentence(companies, industries, label_to_provider)
        assert result == "Syracuse 1st in both query types."

    def test_different_winners(self):
        companies = {"ranking": ["A", "B"]}
        industries = {"ranking": ["C", "A"]}
        label_to_provider = {"A": "Syracuse", "B": "Perplexity", "C": "Exa"}
        result = _headline_sentence(companies, industries, label_to_provider)
        assert result == (
            "No single winner: Syracuse 1st for companies, Exa 1st for industries."
        )


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
        lines = _format_article(2, self._art(), REF, markers=["DUP of #1"])
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
        lines, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=3)
        shown = [l for l in lines if l.strip().startswith(tuple("0123456789"))]
        assert len(shown) <= 3
        assert any("more articles not shown" in l for l in lines)

    def test_counts_dups(self):
        arts = self._make_articles(2)
        arts[1]["document_url"] = arts[0]["document_url"]  # force dup
        _, dup_count, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert dup_count == 1

    def test_no_articles(self):
        lines, dup_count, _ = _render_item("Company", "Acme", [], [], REF, max_articles=15)
        assert any("NO RESULTS RETURNED" in l for l in lines)
        assert dup_count == 0


# ---------------------------------------------------------------------------
# classify_publisher / no-publisher reporting
# ---------------------------------------------------------------------------

class TestClassifyPublisher:
    def test_published(self):
        assert classify_publisher({"published_by": "Reuters"}) == "published"

    def test_missing_key(self):
        assert classify_publisher({}) == "no_publisher"

    def test_empty_string(self):
        assert classify_publisher({"published_by": ""}) == "no_publisher"

    def test_whitespace_only(self):
        assert classify_publisher({"published_by": "   "}) == "no_publisher"

    def test_none_value(self):
        # CSV round-trips can yield None rather than ""
        assert classify_publisher({"published_by": None}) == "no_publisher"

    def test_domain_does_not_count_as_a_publisher(self):
        # A domain is derivable from any URL — crediting it would score every
        # provider identically and measure nothing.
        art = {"published_by": "", "document_url": "https://www.reuters.com/x"}
        assert classify_publisher(art) == "no_publisher"


class TestNoPublisherRendering:
    def _art(self, source, url="https://www.example.com/x"):
        return {
            "published_date_clean": "2026-04-10T00:00:00+00:00",
            "headline": "Acme Q1 results",
            "published_by": source,
            "document_url": url,
            "summary_text": "Acme reported strong earnings.",
        }

    def test_no_publisher_flag_shown(self):
        lines = _format_article(1, self._art(""), REF)
        assert "NO PUBLISHER" in lines[0]

    def test_domain_shown_alongside_missing_publisher(self):
        # The judge must see the domain, since that is why a missing publisher
        # is weighted below a missing date.
        lines = _format_article(1, self._art("", "https://www.reuters.com/x"), REF)
        assert "NO PUBLISHER ⚠ (reuters.com)" in lines[0]

    def test_domain_shown_alongside_present_publisher(self):
        lines = _format_article(1, self._art("Reuters", "https://www.reuters.com/x"), REF)
        assert "| Reuters (reuters.com)" in lines[0]
        assert "NO PUBLISHER" not in lines[0]

    def test_no_domain_parens_when_url_missing(self):
        lines = _format_article(1, self._art("", ""), REF)
        assert "NO PUBLISHER ⚠" in lines[0]
        assert "()" not in lines[0]

    def test_stored_domain_column_preferred(self):
        art = self._art("", "https://www.example.com/x")
        art["publisher_domain"] = "override.com"
        assert "(override.com)" in _format_article(1, art, REF)[0]

    def test_item_header_counts_no_publisher(self):
        arts = [self._art(""), self._art(""), self._art("Reuters")]
        lines, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert "2 no-publisher" in lines[0]

    def test_item_header_omits_when_all_published(self):
        arts = [self._art("Reuters")]
        lines, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert "no-publisher" not in lines[0]

    def test_unrelated_headlines_not_dup_when_publisher_blank(self):
        arts = [self._art("", "https://reuters.com/a"),
                self._art("", "https://apnews.com/b")]
        arts[1]["headline"] = "Gamma opens new plant"
        _, dup_count, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
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

    def test_no_publisher_in_provider_header(self):
        def _row(source, url):
            return {
                "provider": "Perplexity Search", "company": "Acme",
                "headline": f"Acme news {url}", "published_by": source,
                "published_date_clean": "2026-04-10T00:00:00+00:00",
                "published_date": "", "document_url": url,
                "summary_text": "", "industry": "", "location": "", "activity_type": "",
            }
        rows = [_row("", "https://example.com/1"),
                _row("", "https://example.com/2"),
                _row("Reuters", "https://reuters.com/3")]
        _, p2l = make_anonymization(["Perplexity Search"])
        out = format_companies_data(rows, p2l, max_articles=15, reference_date=REF)
        assert "no-publisher: 2 (67%)" in out


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


# ---------------------------------------------------------------------------
# Spelling variants
# ---------------------------------------------------------------------------

def _crow(company, url, provider="Exa", headline=None):
    return {
        "provider": provider, "company": company,
        "headline": headline or f"{company} news {url}", "published_by": "Reuters",
        "published_date_clean": "2026-04-10T00:00:00+00:00",
        "published_date": "", "document_url": url,
        "summary_text": "", "industry": "", "location": "", "activity_type": "",
    }


class TestVariantKey:
    def test_folds_accents_case_and_punctuation(self):
        assert _variant_key("Klöckner Pentaplast") == _variant_key("Klockner Pentaplast")
        assert _variant_key("KLOCKNER-PENTAPLAST") == _variant_key("Klockner Pentaplast")

    def test_distinct_names_do_not_collide(self):
        assert _variant_key("Borouge") != _variant_key("Borealis")

    def test_empty_name(self):
        assert _variant_key("") == ""


class TestVariantGroups:
    def test_groups_variants_and_drops_singletons(self):
        groups = _variant_groups(["Klöckner Pentaplast", "Klockner Pentaplast", "Borouge"])
        assert groups == [["Klockner Pentaplast", "Klöckner Pentaplast"]]

    def test_no_variants_returns_empty(self):
        assert _variant_groups(["Borouge", "Westrock"]) == []


class TestVariantConsistency:
    def test_overlap_and_counts(self):
        rows = [
            _crow("Klöckner Pentaplast", "https://r.com/a"),
            _crow("Klöckner Pentaplast", "https://r.com/b"),
            _crow("Klockner Pentaplast", "https://r.com/a"),
        ]
        _, p2l = make_anonymization(["Exa"])
        groups = variant_consistency(group_rows(rows, p2l, "companies"))
        assert len(groups) == 1
        stats = groups[0]["providers"]["A"]
        # variants are sorted: unaccented first
        assert stats["counts"] == [1, 2]
        assert stats["shared"] == 1
        assert stats["union"] == 2
        assert stats["overlap"] == 0.5

    def test_identical_results_score_one(self):
        rows = [
            _crow("Klöckner Pentaplast", "https://r.com/a"),
            _crow("Klockner Pentaplast", "https://r.com/a"),
        ]
        _, p2l = make_anonymization(["Exa"])
        stats = variant_consistency(group_rows(rows, p2l, "companies"))[0]["providers"]["A"]
        assert stats["overlap"] == 1.0
        assert "spelling-insensitive" in variant_block(
            variant_consistency(group_rows(rows, p2l, "companies")), "Company"
        )

    def test_answers_only_one_spelling_is_flagged(self):
        """Exa answers both spellings; Linkup only the accented one. The pair is
        visible because some provider returned rows for each spelling."""
        rows = [
            _crow("Klöckner Pentaplast", "https://r.com/a"),
            _crow("Klockner Pentaplast", "https://r.com/a"),
            _crow("Klöckner Pentaplast", "https://r.com/b", provider="Linkup"),
        ]
        _, p2l = make_anonymization(["Exa", "Linkup"])
        groups = variant_consistency(group_rows(rows, p2l, "companies"))
        stats = groups[0]["providers"][p2l["Linkup"]]
        assert stats["counts"] == [0, 1]
        assert stats["overlap"] == 0.0
        assert stats["answered"] == ["Klöckner Pentaplast"]
        assert "answers only" in variant_block(groups, "Company")

    def test_pair_needs_both_spellings_in_the_run(self):
        """A spelling no provider returned anything for leaves no CSV rows, so
        the pair cannot be detected — documented limitation, asserted here."""
        rows = [_crow("Klöckner Pentaplast", "https://r.com/a")]
        _, p2l = make_anonymization(["Exa"])
        assert variant_consistency(group_rows(rows, p2l, "companies")) == []

    def test_error_only_spelling_still_forms_a_pair(self):
        """An all-errors spelling does leave rows, so the pair stays visible."""
        rows = [
            _crow("Klöckner Pentaplast", "https://r.com/a"),
            _crow("Klockner Pentaplast", "", headline="*** ERROR ***"),
        ]
        _, p2l = make_anonymization(["Exa"])
        groups = variant_consistency(group_rows(rows, p2l, "companies"))
        assert len(groups) == 1
        assert groups[0]["providers"]["A"]["counts"] == [0, 1]

    def test_error_rows_are_excluded(self):
        rows = [
            _crow("Klöckner Pentaplast", "", headline="*** ERROR ***"),
            _crow("Klockner Pentaplast", "https://r.com/a"),
        ]
        _, p2l = make_anonymization(["Exa"])
        stats = variant_consistency(group_rows(rows, p2l, "companies"))[0]["providers"]["A"]
        assert stats["counts"] == [1, 0]

    def test_no_pairs_yields_no_section(self):
        rows = [_crow("Borouge", "https://r.com/a")]
        _, p2l = make_anonymization(["Exa"])
        groups = variant_consistency(group_rows(rows, p2l, "companies"))
        assert groups == []
        assert variant_block(groups, "Company") == ""
        assert variant_table_md(groups, {"A": "Exa"}) == ""


class TestVariantRendering:
    def test_section_appears_in_prompt_data(self):
        rows = [
            _crow("Klöckner Pentaplast", "https://r.com/a"),
            _crow("Klockner Pentaplast", "https://r.com/b"),
        ]
        _, p2l = make_anonymization(["Exa"])
        out = format_companies_data(rows, p2l, max_articles=15, reference_date=REF)
        assert "SPELLING-VARIANT CONSISTENCY" in out
        assert "overlap 0%" in out

    def test_section_absent_without_pairs(self):
        rows = [_crow("Borouge", "https://r.com/a")]
        _, p2l = make_anonymization(["Exa"])
        out = format_companies_data(rows, p2l, max_articles=15, reference_date=REF)
        assert "SPELLING-VARIANT CONSISTENCY" not in out

    def test_table_decodes_provider_names(self):
        rows = [
            _crow("Klöckner Pentaplast", "https://r.com/a"),
            _crow("Klockner Pentaplast", "https://r.com/a"),
        ]
        _, p2l = make_anonymization(["Exa"])
        groups = variant_consistency(group_rows(rows, p2l, "companies"))
        table = variant_table_md(groups, {"A": "Exa"})
        assert "| Exa |" in table
        assert "100%" in table


class TestVariantEvidenceIndex:
    def test_citing_the_other_spelling_is_not_a_hallucination(self):
        """A provider that answered only the accented spelling may legitimately
        be discussed under the unaccented one — they are the same entity."""
        rows = [_crow("Klöckner Pentaplast", "https://r.com/a")]
        _, p2l = make_anonymization(["Exa"])
        alias_map, answered = build_evidence_index(rows, p2l, "companies")
        scorecard = {"providers": [{
            "label": "A",
            "axes": {"precision": {"score": 5, "evidence": [
                "Klockner Pentaplast: returned a clean Reuters item"]}},
        }]}
        assert verify_evidence(scorecard, alias_map, answered) == 0

    def test_unrelated_entity_still_warns(self):
        rows = [_crow("Klöckner Pentaplast", "https://r.com/a")]
        _, p2l = make_anonymization(["Exa"])
        alias_map, answered = build_evidence_index(rows, p2l, "companies")
        alias_map["borouge"] = {"borouge"}
        scorecard = {"providers": [{
            "label": "A",
            "axes": {"precision": {"score": 5, "evidence": ["Borouge: invented example"]}},
        }]}
        assert verify_evidence(scorecard, alias_map, answered) == 1


# --- Provider self-reported relevance --------------------------------------


def _srow(company, url, score, provider="Tavily", headline=None):
    row = _crow(company, url, provider=provider, headline=headline)
    row["relevance_score"] = "" if score is None else str(score)
    return row


def _diag(rows):
    data = group_rows(rows, {"Tavily": "A", "Exa": "B"}, "companies")
    return score_diagnostics(data)


class TestScoreOf:
    def test_parses_a_string_score(self):
        assert _score_of({"relevance_score": "0.42"}) == 0.42

    def test_blank_and_missing_are_none(self):
        assert _score_of({"relevance_score": ""}) is None
        assert _score_of({}) is None

    def test_unparseable_is_none_not_an_error(self):
        assert _score_of({"relevance_score": "n/a"}) is None

    def test_zero_is_a_score_not_a_missing_value(self):
        # 0.0 is falsy; a provider scoring a result 0 has still scored it.
        assert _score_of({"relevance_score": "0.0"}) == 0.0


class TestScoreDiagnostics:
    def test_provider_with_no_scores_is_reported_not_omitted(self):
        diag = _diag([_srow("Acme", "https://a.com/1", None, provider="Exa")])
        assert diag["B"]["scored"] == 0
        assert diag["B"]["total"] == 1
        assert diag["B"]["median"] is None

    def test_counts_and_median(self):
        diag = _diag([
            _srow("Acme", "https://a.com/1", 0.1),
            _srow("Acme", "https://a.com/2", 0.3),
            _srow("Acme", "https://a.com/3", 0.5),
        ])
        assert diag["A"]["scored"] == 3
        assert diag["A"]["median"] == 0.3

    def test_item_whose_best_score_is_weak_is_flagged(self):
        diag = _diag([
            _srow("Acme", "https://a.com/1", 0.05),
            _srow("Acme", "https://a.com/2", 0.11),
        ])
        assert [n for n, _, _ in diag["A"]["weak_items"]] == ["Acme"]
        assert diag["A"]["weak_items"][0][1] == 2      # articles returned
        assert diag["A"]["weak_items"][0][2] == 0.11   # best score

    def test_item_with_one_strong_result_is_not_weak(self):
        diag = _diag([
            _srow("Acme", "https://a.com/1", 0.05),
            _srow("Acme", "https://a.com/2", 0.9),
        ])
        assert diag["A"]["weak_items"] == []
        assert diag["A"]["weak"] == 1  # the individual weak article still counts

    def test_error_rows_are_excluded(self):
        err = _srow("Acme", "https://a.com/1", None, headline="*** ERROR ***")
        diag = _diag([err, _srow("Acme", "https://a.com/2", 0.4)])
        assert diag["A"]["total"] == 1
        assert diag["A"]["scored"] == 1

    def test_unscored_provider_never_produces_weak_items(self):
        # A provider that returns no score must not be accused of returning
        # results it knew were weak - it made no claim either way.
        diag = _diag([_srow("Acme", f"https://a.com/{i}", None, provider="Exa")
                      for i in range(5)])
        assert diag["B"]["weak_items"] == []


class TestScoreRendering:
    def test_block_is_empty_when_nobody_scores(self):
        diag = _diag([_srow("Acme", "https://a.com/1", None, provider="Exa")])
        assert score_block(diag, "Company") == ""
        assert score_table_md(diag, {"B": "Exa"}) == ""

    def test_block_names_weak_items_and_says_it_does_not_filter(self):
        diag = _diag([
            _srow("Acme", "https://a.com/1", 0.02),
            _srow("Acme", "https://a.com/2", 0.03),
        ])
        out = score_block(diag, "Company")
        assert "PROVIDER SELF-REPORTED RELEVANCE" in out
        assert "NOT used to filter" in out
        assert "Acme" in out
        assert "best score only 0.030" in out

    def test_unscored_provider_reported_as_a_limitation(self):
        diag = _diag([
            _srow("Acme", "https://a.com/1", 0.4),
            _srow("Acme", "https://b.com/1", None, provider="Exa"),
        ])
        out = score_block(diag, "Company")
        assert "PROVIDER B: returns no relevance score" in out

    def test_table_decodes_provider_names(self):
        diag = _diag([_srow("Acme", "https://a.com/1", 0.02)])
        md = score_table_md(diag, {"A": "Tavily", "B": "Exa"})
        assert "| Tavily |" in md
        assert "A" not in md.split("|")[1]

    def test_weak_threshold_is_the_documented_one(self):
        # The prompt text quotes WEAK_SCORE; they must not drift apart.
        diag = _diag([_srow("Acme", "https://a.com/1", 0.02)])
        assert f"below {WEAK_SCORE}" in score_block(diag, "Company")
