from tavily import TavilyClient
from utils import TAVILY_API_KEY, MAX_DATE, MIN_DATE, log_error
from queries import company_keyword_query, industry_keyword_query
import json
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

PROVIDER_NAME = "Tavily"

def get_industry_articles_for(industry: str, industry_context: str, location: str):
    query = industry_query(industry, industry_context, location)
    query_context = f"industry={industry}, industry_context={industry_context}, location={location}"
    results = do_query(query, query_context)
    articles = []
    for item in results['results']:
        article = item_to_article(item, query_context)
        articles.append(article)
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def get_company_articles_for(company: str):
    query = company_query(company)
    query_context = f"company={company}"
    results = do_query(query, query_context)
    articles = []
    for item in results['results']:
        article = item_to_article(item, query_context)
        articles.append(article)
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def industry_query(industry, industry_context, location):
    return industry_keyword_query(industry, industry_context, location)

def company_query(company_name):
    return company_keyword_query(company_name)

def do_query(query, query_context):
    if TAVILY_API_KEY is None or TAVILY_API_KEY.strip() == '' or TAVILY_API_KEY == 'my_tavily_key':
        return {'results':[]}
    
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query=query[:400],
            search_depth="advanced",
            max_results=20,
            topic="news",
            start_date=MIN_DATE.date().isoformat(),
            end_date=MAX_DATE.date().isoformat(),
            )
        return response
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"query": query[:400]})
        return {'results': []}

def parse_published_date(raw: str, query_context: str):
    """Tavily returns published_date only when topic="news" (its docs: "Set to
    news for news sources (includes published_date metadata)"). The format is
    not contractually fixed, so try ISO 8601 then RFC 2822 before giving up.
    An unparseable date is blank, not an error row — same as a genuinely absent
    one."""
    if not raw:
        return ""
    for parser in (datetime.fromisoformat, parsedate_to_datetime):
        try:
            parsed = parser(raw)
        except Exception:
            continue
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    log_error(PROVIDER_NAME, "PARSE_DATE", query_context,
              f"unrecognised published_date format: {raw!r}", {"published_date": raw})
    return ""


def item_to_article(item: dict, query_context: str):
    try:
        published_date = item.get('published_date') or ""
        return {
            "headline": item['title'],
            "published_date_clean": parse_published_date(published_date, query_context),
            "published_date": published_date,
            "summary_text": item['content'].replace("\n"," ")[:1000],
            "published_by": "",
            "document_url": item['url'],
        }
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_ARTICLE", query_context, str(e), item)
        return {
            "headline": "*** ERROR ***",
            "summary_text": str(e),
            "published_date": "",
            "published_date_clean": "",
            "published_by": "",
            "document_url": item.get('url', 'unknown'),
        }