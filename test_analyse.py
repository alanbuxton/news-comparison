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
    _is_not_news,
    WEAK_SCORE,
    _score_of,
    _variant_groups,
    _variant_key,
    build_evidence_index,
    COMPANIES_PROMPT,
    INDUSTRIES_PROMPT,
    README_SUMMARY_PROMPT,
    SYSTEM_PROMPT,
    classify_date,
    PADDED_ITEM_PENALTY,
    apply_company_metrics,
    bootstrap_company_metrics,
    bootstrap_md,
    build_label_request,
    company_metrics_md,
    company_row_metrics,
    load_query_manifest,
    parse_label_response,
    split_controls,
    classify_publisher,
    format_companies_data,
    group_rows,
    make_anonymization,
    fill_provider_counts,
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
        lines, _, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=3)
        shown = [l for l in lines if l.strip().startswith(tuple("0123456789"))]
        assert len(shown) <= 3
        assert any("more articles not shown" in l for l in lines)

    def test_counts_dups(self):
        arts = self._make_articles(2)
        arts[1]["document_url"] = arts[0]["document_url"]  # force dup
        _, dup_count, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert dup_count == 1

    def test_no_articles(self):
        lines, dup_count, _, _ = _render_item("Company", "Acme", [], [], REF, max_articles=15)
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
        lines, _, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert "2 no-publisher" in lines[0]

    def test_item_header_omits_when_all_published(self):
        arts = [self._art("Reuters")]
        lines, _, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
        assert "no-publisher" not in lines[0]

    def test_unrelated_headlines_not_dup_when_publisher_blank(self):
        arts = [self._art("", "https://reuters.com/a"),
                self._art("", "https://apnews.com/b")]
        arts[1]["headline"] = "Gamma opens new plant"
        _, dup_count, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=15)
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

    def test_six_providers_get_six_letters(self):
        providers = [
            "Exa", "Linkup", "Perplexity Agent", "Perplexity Search",
            "Syracuse", "Tavily",
        ]
        l2p, _ = make_anonymization(providers)
        assert set(l2p.keys()) == set("ABCDEF")
        assert set(l2p.values()) == set(providers)


# ---------------------------------------------------------------------------
# fill_provider_counts
# ---------------------------------------------------------------------------

class TestFillProviderCounts:
    TEMPLATE = (
        "__N_PROVIDERS_CAP__ providers (labelled __LABELS__). "
        "Treat __LABEL_LIST__ alike. Cover all __N_PROVIDERS__ providers."
    )

    def test_five_providers(self):
        out = fill_provider_counts(self.TEMPLATE, list("ABCDE"))
        assert out == (
            "Five providers (labelled A\u2013E). "
            "Treat A, B, C, D, E alike. Cover all five providers."
        )

    def test_six_providers(self):
        out = fill_provider_counts(self.TEMPLATE, list("ABCDEF"))
        assert "Six providers (labelled A\u2013F)" in out
        assert "Treat A, B, C, D, E, F alike" in out
        assert "all six providers" in out

    def test_single_provider_has_no_range(self):
        out = fill_provider_counts(self.TEMPLATE, ["A"])
        assert "labelled A)" in out
        assert "\u2013" not in out

    def test_prompts_carry_no_hardcoded_count(self):
        for prompt in (SYSTEM_PROMPT, COMPANIES_PROMPT, INDUSTRIES_PROMPT,
                       README_SUMMARY_PROMPT):
            filled = fill_provider_counts(prompt, list("ABCDEF"))
            assert "A\u2013E" not in filled
            assert "five providers" not in filled
            assert "Five news search providers" not in filled


class TestNotNews:
    """Social posts, forum threads, videos and company About pages are FP-not-news
    under the rubric. Flagged by the harness, like market reports, so the count is
    the same however the judge reads the rows, and covers rows past the shown cap."""

    def _art(self, url, headline="Acme news"):
        return {"published_date_clean": "2026-04-10T00:00:00+00:00", "headline": headline,
                "published_by": "", "document_url": url, "summary_text": "s"}

    @pytest.mark.parametrize("url", [
        "https://www.facebook.com/acme/posts/123",
        "https://m.facebook.com/story.php?id=1",
        "https://uk.linkedin.com/posts/acme_launch-activity-1",
        "https://x.com/acme/status/1",
        "https://www.reddit.com/r/plastics/comments/abc",
        "https://www.youtube.com/watch?v=abc",
        "https://acme.com/about-us",
        "https://www.acme.com/en/company/about/",
        "https://acme.com/who-we-are",
    ])
    def test_flags_social_posts_and_about_pages(self, url):
        assert _is_not_news(self._art(url))

    @pytest.mark.parametrize("url", [
        "https://www.reuters.com/business/acme-buys-rival-2026-04-10/",
        "https://economictimes.indiatimes.com/news/company/corporate-trends/acme/articleshow/1.cms",
        "https://www.bloomberg.com/news/articles/2026-04-10/acme-about-to-list",
        "https://notfacebook.com/acme",
        "https://www.acme.com/about-us/news/2026/acme-opens-plant",
        "https://acme.com/about/press-releases/q1-results",
        "https://www.linklaters.com/about-us/news-and-deals/deals/2026/august/linklaters-advises-x",
        "https://www.deloitte.com/us/en/about/press-room/deloitte-announces-ma-platform.html",
        "https://www.uwstout.edu/about-us/news-center/university-partner-award-green-bay-packaging",
    ])
    def test_leaves_news_alone(self, url):
        assert not _is_not_news(self._art(url))

    def test_flagged_inline_and_counted_beyond_the_shown_cap(self):
        arts = [self._art(f"https://reuters.com/{i}", f"Headline {i}") for i in range(3)]
        arts.append(self._art("https://www.facebook.com/acme/posts/1", "Hidden post"))
        lines, _, _, not_news = _render_item("Company", "Acme", arts, [], REF, max_articles=3)
        assert not_news == 1
        assert "1 not-news" in lines[0]
        arts.insert(0, arts.pop())
        lines, _, _, _ = _render_item("Company", "Acme", arts, [], REF, max_articles=3)
        assert any("[NOT-NEWS ⚠] Hidden post" in l for l in lines)

    def test_provider_header_carries_the_count(self):
        rows = [{"provider": "Exa", "company": "Acme", **self._art("https://x.com/acme/status/1")}]
        out = format_companies_data(rows, {"Exa": "A"}, 20, REF)
        assert "not-news: 1 (100%)" in out

    def test_judge_is_told_the_flag_is_ground_truth_and_costs_precision(self):
        system = " ".join(SYSTEM_PROMPT.split())
        assert "`[NOT-NEWS ⚠]` flags and the `not-news: N` header count" in system
        for prompt in (COMPANIES_PROMPT, INDUSTRIES_PROMPT):
            assert "[NOT-NEWS ⚠]" in prompt
            assert "FP-not-news" in prompt


class TestProviderTextIsClaims:
    """Only the harness's flags are ground truth. Everything a provider returns —
    headline, summary, publisher, any label — is that provider's claim, whoever the
    provider is: an LLM summary can invent facts, and a confident label can make a
    wrong-entity row look relevant. The rule names no provider's format."""

    def test_every_provider_field_is_a_claim(self):
        prompt = " ".join(SYSTEM_PROMPT.split())
        assert "is that provider's claim, not ground truth, whichever provider" in prompt
        assert "headline, summary, publisher, and any label or note" in prompt

    def test_rule_is_not_shaped_to_one_provider(self):
        assert "bracketed" not in SYSTEM_PROMPT


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


# ---------------------------------------------------------------------------
# Company row labels, controls and harness-computed precision/coverage
# ---------------------------------------------------------------------------

def _groups(rows):
    return group_rows(rows, {"Exa": "A", "Perplexity Agent": "B"}, "companies")


def _zeta(n, provider="Perplexity Agent", stem="Zeta Global story"):
    return [_crow("ZETA TECHNICAL SERVICES", f"https://z.com/{i}", provider=provider,
                  headline=f"{stem} number {i}") for i in range(n)]


def _labels(**by_company):
    """_labels(B={"Acme": ["on_target", "wrong_entity"]}) → row_labels shape."""
    return {
        prov: {name: [None if l is None else {"label": l, "about": ""} for l in ls]
               for name, ls in items.items()}
        for prov, items in by_company.items()
    }


class TestQueryManifest:
    def test_missing_manifest_means_no_profiles_or_controls(self, tmp_path):
        m = load_query_manifest(str(tmp_path))
        assert m == {"profiles": {}, "controls": set(), "queried": None}

    def test_reads_profiles_controls_and_queried(self, tmp_path):
        (tmp_path / "queries.json").write_text(json.dumps({"companies": [
            {"name": "Acme", "profile": "Widget maker", "control": False},
            {"name": "Nobody", "profile": "", "control": False},
            {"name": "Korvessa", "profile": "", "control": True},
        ]}))
        m = load_query_manifest(str(tmp_path))
        assert m["profiles"] == {"Acme": "Widget maker"}
        assert m["controls"] == {"Korvessa"}
        assert m["queried"] == ["Acme", "Nobody"]

    def test_backfilled_manifest_is_profiles_only(self, tmp_path):
        (tmp_path / "queries.json").write_text(json.dumps({"backfilled": True, "companies": [
            {"name": "Acme", "profile": "Widget maker", "control": False}]}))
        assert load_query_manifest(str(tmp_path))["queried"] is None


class TestSplitControls:
    def test_controls_leave_judge_data(self):
        rows = _zeta(1) + [_crow("Korvessa", "https://k.com/1", provider="Exa")]
        real, ctrl = split_controls(_groups(rows), {"Korvessa"})
        assert "Korvessa" not in real["A"] and "Korvessa" in ctrl["A"]
        assert "A" in real  # provider still present even if it only hit a control

    def test_judge_never_sees_control_names(self):
        rows = _zeta(1) + [_crow("Korvessa", "https://k.com/1", provider="Exa")]
        text = format_companies_data(rows, {"Exa": "A", "Perplexity Agent": "B"}, 20, REF,
                                     controls={"Korvessa"})
        assert "Korvessa" not in text


class TestLabelRequest:
    def test_rows_are_shuffled_under_opaque_ids_and_mapped_back(self):
        rows = _zeta(3) + _zeta(2, provider="Exa")
        prompt, id_map = build_label_request("ZETA TECHNICAL SERVICES", "", _groups(rows), 20)
        assert sorted(id_map.values()) == [("A", 1), ("A", 2), ("B", 1), ("B", 2), ("B", 3)]
        assert "Provider" not in prompt and "PROVIDER" not in prompt
        assert "none supplied" in prompt

    def test_profile_is_shown(self):
        prompt, _ = build_label_request("ZETA TECHNICAL SERVICES", "Dubai MEP firm",
                                        _groups(_zeta(1)), 20)
        assert "Profile: Dubai MEP firm" in prompt

    def test_only_shown_rows_are_sent(self):
        _, id_map = build_label_request("ZETA TECHNICAL SERVICES", "", _groups(_zeta(5)), 3)
        assert len(id_map) == 3

    def test_deterministic_for_same_name(self):
        g = _groups(_zeta(6) + _zeta(6, provider="Exa"))
        assert build_label_request("ZETA TECHNICAL SERVICES", "", g, 20) == \
            build_label_request("ZETA TECHNICAL SERVICES", "", g, 20)


class TestParseLabelResponse:
    def test_keeps_valid_entries_only(self):
        id_map = {"r1": ("A", 1), "r2": ("A", 2)}
        text = 'Sure:\n{"rows": [{"id": "r1", "label": "wrong_entity", "about": "Zeta Global"},' \
               '{"id": "r2", "label": "maybe"}, {"id": "r9", "label": "on_target"}]}'
        assert parse_label_response(text, id_map) == {
            "r1": {"label": "wrong_entity", "about": "Zeta Global"}}

    def test_garbage_returns_empty(self):
        assert parse_label_response("no json here", {"r1": ("A", 1)}) == {}


class TestCompanyRowMetrics:
    def _m(self, rows, labels, controls=(), queried=None):
        real, ctrl = split_controls(_groups(rows), set(controls))
        return company_row_metrics(real, ctrl, labels, REF, 20, queried)

    def test_padded_company_cancels_an_answered_one(self):
        rows = _zeta(2) + [_crow("Acme", "https://a.com/1", provider="Perplexity Agent")]
        m = self._m(rows, _labels(B={"ZETA TECHNICAL SERVICES": ["wrong_entity"] * 2,
                                      "Acme": ["on_target"]}))["B"]
        assert m["answered"] == 1 and len(m["padded"]) == 1
        assert m["coverage"] == round(10 * (1 - PADDED_ITEM_PENALTY) / 2, 1)
        assert m["precision"] == round(10 * 1 / 3, 1)

    def test_padding_scores_below_silence(self):
        # Same answered company; one provider pads a second, the other is silent.
        rows = ([_crow("Acme", "https://a.com/1", provider="Perplexity Agent")] + _zeta(2)
                + [_crow("Acme", "https://a.com/2", provider="Exa")])
        m = self._m(rows, _labels(B={"Acme": ["on_target"],
                                      "ZETA TECHNICAL SERVICES": ["wrong_entity"] * 2},
                                   A={"Acme": ["on_target"]}))
        assert m["B"]["coverage"] < m["A"]["coverage"]

    def test_control_hits_count_against_precision_and_coverage(self):
        rows = [_crow("Acme", "https://a.com/1", provider="Exa"),
                _crow("Korvessa", "https://k.com/1", provider="Exa"),
                _crow("Korvessa", "https://k.com/2", provider="Exa")]
        m = self._m(rows, _labels(A={"Acme": ["on_target"]}), controls={"Korvessa"})["A"]
        assert m["control_rows"] == 2 and len(m["control_hits"]) == 1
        assert m["precision"] == round(10 / 3, 1)
        assert m["coverage"] == 0.0  # 1 answered − 1 control hit, out of 1 company

    def test_duplicate_on_target_row_is_not_clean(self):
        rows = [_crow("Acme", "https://a.com/1", provider="Exa", headline="Acme buys Beta"),
                _crow("Acme", "https://b.com/1", provider="Exa", headline="Acme buys Beta")]
        m = self._m(rows, _labels(A={"Acme": ["on_target", "on_target"]}))["A"]
        assert m["clean"] == 1 and m["flagged"] == 1

    def test_unlabelled_rows_leave_the_denominator(self):
        rows = [_crow("Acme", f"https://a.com/{i}", provider="Exa") for i in range(2)]
        m = self._m(rows, _labels(A={"Acme": ["on_target", None]}))["A"]
        assert m["unlabelled"] == 1 and m["precision"] == 10.0

    def test_queried_company_nobody_answered_counts_in_universe(self):
        rows = [_crow("Acme", "https://a.com/1", provider="Exa")]
        m = self._m(rows, _labels(A={"Acme": ["on_target"]}), queried=["Acme", "Ghost"])["A"]
        assert m["universe"] == 2 and m["coverage"] == 5.0

    def test_no_rows_means_precision_zero(self):
        rows = [_crow("Acme", "https://a.com/1", provider="Exa", headline="*** ERROR ***")]
        assert self._m(rows, {})["A"]["precision"] == 0.0


class TestApplyCompanyMetrics:
    def test_replaces_scores_keeps_judge_view_and_reranks(self):
        card = {"providers": [_prov(precision=9, label="A"), _prov(precision=5, label="B")]}
        metrics = {
            "A": dict(precision=2.0, coverage=5.0, clean=1, labelled_rows=5, wrong_entity=4,
                      name_drop=0, not_news=0, flagged=0, control_rows=0, answered=1,
                      universe=2, padded=[], control_hits=[]),
            "B": dict(precision=9.0, coverage=7.0, clean=9, labelled_rows=10, wrong_entity=1,
                      name_drop=0, not_news=0, flagged=0, control_rows=0, answered=2,
                      universe=2, padded=[], control_hits=[]),
        }
        apply_company_metrics(card, metrics)
        a = next(p for p in card["providers"] if p["label"] == "A")
        assert a["axes"]["precision"]["score"] == 2.0
        assert a["axes"]["precision"]["judge_score"] == 9
        assert "precision" in a["caps_applied"]
        assert card["ranking"] == ["B", "A"]


def _metrics_from(per_item_by_label):
    """Metrics in company_row_metrics' shape from {label: {company: (clean, labelled)}}."""
    out = {}
    for lb, items in per_item_by_label.items():
        per_item = {n: {"clean": c, "labelled": l} for n, (c, l) in items.items()}
        clean = sum(c for c, _ in items.values())
        labelled = sum(l for _, l in items.values())
        out[lb] = dict(precision=round(10 * clean / labelled, 1) if labelled else 0.0,
                       coverage=0.0, per_item=per_item, control_rows=0, control_hits=[])
    return out


def _ranked_card(metrics):
    card = {"providers": [_prov(precision=m["precision"], label=lb)
                          for lb, m in metrics.items()]}
    from analyse import _recompute_provider, _rank_providers
    for p in card["providers"]:
        _recompute_provider(p)
    return _rank_providers(card)


class TestBootstrap:
    def test_per_item_tallies_match_answered_and_padded(self):
        rows = _zeta(2) + [_crow("Acme", "https://a.com/1", provider="Perplexity Agent")]
        real, ctrl = split_controls(_groups(rows), set())
        m = company_row_metrics(real, ctrl, _labels(B={
            "ZETA TECHNICAL SERVICES": ["wrong_entity"] * 2, "Acme": ["on_target"]}),
            REF, 20)["B"]
        assert m["per_item"] == {"Acme": {"clean": 1, "labelled": 1},
                                 "ZETA TECHNICAL SERVICES": {"clean": 0, "labelled": 2}}

    def test_clear_winner_is_separated(self):
        names = [f"C{i}" for i in range(30)]
        metrics = _metrics_from({"A": {n: (5, 5) for n in names},
                                 "B": {n: (1, 5) for n in names}})
        boot = bootstrap_company_metrics(metrics, _ranked_card(metrics), resamples=200)
        assert boot["A"]["rank"] == 1 and boot["A"]["ahead_of_next"] == 1.0
        assert boot["A"]["held_rank"] == 1.0
        assert boot["B"]["ahead_of_next"] is None

    def test_near_tie_is_not_separated_and_marked(self):
        names = [f"C{i}" for i in range(30)]
        # A and B are equally good overall, but on different companies.
        a = {n: ((5, 5) if i % 2 else (2, 5)) for i, n in enumerate(names)}
        b = {n: ((2, 5) if i % 2 else (5, 5)) for i, n in enumerate(names)}
        metrics = _metrics_from({"A": a, "B": b})
        card = _ranked_card(metrics)
        boot = bootstrap_company_metrics(metrics, card, resamples=200)
        top = card["ranking"][0]
        assert boot[top]["ahead_of_next"] < 0.9
        assert "(not separated)" in bootstrap_md(boot, card, {"A": "Exa", "B": "Syracuse"})

    def test_point_estimate_inside_range_and_deterministic(self):
        names = [f"C{i}" for i in range(20)]
        metrics = _metrics_from({"A": {n: (i % 4, 4) for i, n in enumerate(names)}})
        card = _ranked_card(metrics)
        boot = bootstrap_company_metrics(metrics, card, resamples=300)
        lo, hi = boot["A"]["precision_range"]
        assert lo <= metrics["A"]["precision"] <= hi
        assert boot == bootstrap_company_metrics(metrics, card, resamples=300)

    def test_no_companies_means_no_bootstrap(self):
        assert bootstrap_company_metrics({}, {"providers": []}) == {}


class TestControlNames:
    def test_distinct_and_never_a_real_queried_name(self):
        import random
        from examples import company_name_examples, make_control_companies
        real = {n.lower() for n in company_name_examples}
        for seed in range(50):
            names = make_control_companies(random.Random(seed), 3)
            assert len(set(names)) == 3
            assert not real & {n.lower() for n in names}

    def test_main_draws_fresh_names_rather_than_a_fixed_list(self):
        import examples
        assert not hasattr(examples, "control_companies")


class TestCompanyLabelRendering:
    def test_judge_sees_profile_and_label_markers(self):
        rows = _zeta(2)
        text = format_companies_data(
            rows, {"Perplexity Agent": "B"}, 20, REF,
            profiles={"ZETA TECHNICAL SERVICES": "Technical services firm"},
            row_labels={"B": {"ZETA TECHNICAL SERVICES": [
                {"label": "wrong_entity", "about": "Zeta Global"}, None]}},
        )
        assert "Profile: Technical services firm" in text
        assert "[WRONG ENTITY: Zeta Global ⚠]" in text

    def test_prompt_explains_harness_scores_companies(self):
        assert "COMPANY PROFILES AND ROW LABELS" in COMPANIES_PROMPT
        assert "ROW LABELS" not in INDUSTRIES_PROMPT

    def test_report_decodes_and_lists_controls(self):
        rows = [_crow("Korvessa", "https://k.com/1", provider="Exa", headline="Korvessa wins")]
        real, ctrl = split_controls(_groups(rows), {"Korvessa"})
        metrics = company_row_metrics(real, ctrl, {}, REF, 20, ["Acme"])
        card = {"providers": [_prov(label="A")]}
        md = company_metrics_md(metrics, card, {"A": "Exa"})
        assert "| Exa |" in md
        assert "CONTROL Korvessa (made-up): 1 rows — Korvessa wins" in md
        assert "check the headlines" not in md

    def test_control_flagged_only_when_selective_providers_agree(self):
        controls = {"Korvessa", "Draymont"}
        def md_for(rows):
            real, ctrl = split_controls(_groups(rows), controls)
            metrics = company_row_metrics(real, ctrl, {}, REF, 20, ["Acme"])
            card = {"providers": [_prov(label="A"), _prov(label="B")]}
            return company_metrics_md(metrics, card, {"A": "Exa", "B": "Agent"}, controls)
        k = lambda p, i: _crow("Korvessa", f"https://k.com/{p}{i}", provider=p)
        d = lambda p: _crow("Draymont", f"https://d.com/{p}", provider=p)
        # Exa pads every control; only Agent is selective → no flag.
        assert "check the headlines" not in md_for(
            [k("Exa", 1), d("Exa"), k("Perplexity Agent", 1)])
        # Both selective and both answer Korvessa → flag it.
        md = md_for([k("Exa", 1), k("Perplexity Agent", 1), d("Exa"), d("Perplexity Agent")][:2])
        assert md.rstrip().endswith("Korvessa")
