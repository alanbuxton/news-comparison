"""Tests for provider client parsing — pure-Python, no API calls."""

from datetime import datetime, timezone

import pytest

import perplexity_search_client as pxs
import queries as q
import tavily_client as tv
from utils import set_error_log_dir


@pytest.fixture(autouse=True)
def _isolate_error_log(tmp_path):
    """Several of these cases deliberately trip log_error. Without this the logs
    land in the repo's results/errors/ directory."""
    set_error_log_dir(str(tmp_path / "errors"))


# ---------------------------------------------------------------------------
# Tavily date handling
#
# Tavily returns published_date only when topic="news" ("Set to news for news
# sources (includes published_date metadata)"). The client used to hardcode the
# date to "" regardless, which showed up in every past run as Tavily scoring
# 100% no-date. These tests pin the fix.
# ---------------------------------------------------------------------------

class TestTavilyPublishedDate:
    def test_rfc2822(self):
        got = tv.parse_published_date("Wed, 13 Aug 2026 07:00:00 GMT", "ctx")
        assert got == datetime(2026, 8, 13, 7, 0, tzinfo=timezone.utc)

    def test_iso_with_z(self):
        got = tv.parse_published_date("2026-08-13T07:00:00Z", "ctx")
        assert got == datetime(2026, 8, 13, 7, 0, tzinfo=timezone.utc)

    def test_date_only_gets_utc(self):
        got = tv.parse_published_date("2026-08-13", "ctx")
        assert got == datetime(2026, 8, 13, 0, 0, tzinfo=timezone.utc)

    def test_empty_is_blank_not_error(self):
        assert tv.parse_published_date("", "ctx") == ""

    def test_unparseable_is_blank_not_error(self):
        assert tv.parse_published_date("not a date", "ctx") == ""

    def test_article_carries_date_through(self):
        art = tv.item_to_article(
            {"title": "T", "url": "https://x.com/1", "content": "c",
             "published_date": "Wed, 13 Aug 2026 07:00:00 GMT"}, "ctx")
        assert art["published_date"] == "Wed, 13 Aug 2026 07:00:00 GMT"
        assert art["published_date_clean"].year == 2026
        assert art["headline"] != "*** ERROR ***"

    def test_article_without_date_still_parses(self):
        art = tv.item_to_article({"title": "T", "url": "https://x.com/1", "content": "c"}, "ctx")
        assert art["published_date"] == ""
        assert art["published_date_clean"] == ""
        assert art["headline"] == "T"

    def test_missing_title_is_error_row(self):
        art = tv.item_to_article({"url": "https://x.com/1", "content": "c"}, "ctx")
        assert art["headline"] == "*** ERROR ***"
        assert art["document_url"] == "https://x.com/1"


# ---------------------------------------------------------------------------
# Perplexity Search mapping
# ---------------------------------------------------------------------------

class TestPerplexitySearch:
    def _item(self, **kw):
        base = {"title": "T", "url": "https://x.com/1", "snippet": "a\nb",
                "date": "2026-08-01", "last_updated": None}
        base.update(kw)
        return base

    def test_maps_fields(self):
        art = pxs.item_to_article(self._item(), "ctx")
        assert art["headline"] == "T"
        assert art["summary_text"] == "a b"          # newlines flattened
        assert art["published_date_clean"].tzinfo is not None

    def test_null_date_is_blank_not_error(self):
        art = pxs.item_to_article(self._item(date=None), "ctx")
        assert art["published_date"] == ""
        assert art["published_date_clean"] == ""
        assert art["headline"] == "T"

    def test_publisher_always_blank(self):
        # The Search API returns no publisher field at all — this is a real gap
        # that analyse.py scores via no-source, not something to paper over.
        assert pxs.item_to_article(self._item(), "ctx")["published_by"] == ""

    def test_missing_url_is_error_row(self):
        art = pxs.item_to_article({"title": "T", "snippet": "s", "date": None}, "ctx")
        assert art["headline"] == "*** ERROR ***"

    def test_response_without_results_key(self):
        assert pxs.perplexity_response_to_articles({}, "ctx") == []


# ---------------------------------------------------------------------------
# Canonical queries
#
# Company and industry queries are different questions. Normalising them onto a
# single company-shaped topic list ("financial performance", "supplier risk")
# made Linkup return 0 articles for an industry topic that returns ~10 with the
# industry list. These pin the two apart.
# ---------------------------------------------------------------------------

class TestCanonicalQueries:
    def test_topic_lists_are_distinct(self):
        assert q.COMPANY_TOPICS != q.INDUSTRY_TOPICS
        assert q.COMPANY_KEYWORDS != q.INDUSTRY_KEYWORDS

    def test_industry_topics_are_not_company_shaped(self):
        joined = " ".join(q.INDUSTRY_TOPICS).lower()
        for company_term in ("financial performance", "product launches", "supplier risk"):
            assert company_term not in joined

    def test_industry_queries_carry_industry_and_location(self):
        for built in (q.industry_keyword_query("BOPET", "plastic film", "CN"),
                      q.industry_prose_query("BOPET", "plastic film", "CN")):
            assert "BOPET" in built and "CN" in built
            assert "plastic film" in built      # context disambiguates the term

    def test_company_queries_carry_company(self):
        for built in (q.company_keyword_query("Commerzbank"),
                      q.company_prose_query("Commerzbank")):
            assert "Commerzbank" in built

    def test_industry_str_without_context(self):
        assert q.industry_str("PAPER", "") == "PAPER"

    def test_keyword_queries_stay_short(self):
        # Tavily truncates the query at 400 chars.
        built = q.industry_keyword_query("CLEANING SUPPLIES", "janitorial", "New England")
        assert len(built) < 400

    def test_credibility_instruction_reaches_every_prose_query(self):
        assert q.CREDIBILITY in q.company_prose_query("Acme")
        assert q.CREDIBILITY in q.industry_prose_query("PAPER", "", "Europe")

    def test_all_text_clients_use_the_canonical_queries(self):
        import exa_client, tavily_client, perplexity_search_client
        import linkup_client, perplexity_agent_client
        expected_kw = q.company_keyword_query("Acme")
        for mod in (exa_client, tavily_client):
            assert mod.company_query("Acme") == expected_kw
        assert perplexity_search_client.build_company_query("Acme") == expected_kw
        expected_prose = q.company_prose_query("Acme")
        assert linkup_client.company_query("Acme").startswith(expected_prose)
        assert perplexity_agent_client.build_company_user_command("Acme").startswith(expected_prose)
