import requests
from utils import PERPLEXITY_API_KEY, MIN_DATE, MAX_DATE, log_error
from queries import company_keyword_query, industry_keyword_query
from datetime import date, datetime, timezone

PROVIDER_NAME = "Perplexity Search"
PERPLEXITY_ENDPOINT = "https://api.perplexity.ai/search"
MAX_RESULTS = 20  # Search API hard cap is 20 per query

def get_industry_articles_for(industry: str, industry_context: str, location: str):
    query_context = f"industry={industry}, industry_context={industry_context} location={location}"
    query = build_industry_query(industry, industry_context, location)
    response = get_news(query, query_context)
    return perplexity_response_to_articles(response, query_context)

def get_company_articles_for(company: str):
    query_context = f"company={company}"
    query = build_company_query(company)
    response = get_news(query, query_context)
    return perplexity_response_to_articles(response, query_context)

def perplexity_response_to_articles(response, query_context: str):
    try:
        results = response["results"]
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_RESPONSE", query_context, str(e), response)
        return []
    articles = [item_to_article(item, query_context) for item in results]
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def item_to_article(item: dict, query_context: str):
    try:
        published_date = item.get("date") or ""
        return {
            "headline": item["title"],
            "summary_text": (item.get("snippet") or "").replace("\n", " ")[:1000],
            "published_date": published_date,
            "published_date_clean": parse_date(published_date),
            "published_by": "",  # Search API returns no publisher field
            "document_url": item["url"],
        }
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_ARTICLE", query_context, str(e), item)
        return {
            "headline": "*** ERROR ***",
            "summary_text": str(e),
            "published_date": "",
            "published_date_clean": "",
            "published_by": "",
            "document_url": item.get("url", "unknown"),
        }

def parse_date(published_date: str):
    """Search API returns YYYY-MM-DD (or null). Missing dates are blank, not errors."""
    if not published_date:
        return ""
    pub_date = datetime.fromisoformat(published_date)  # Needs Python 3.11 or higher to work
    if isinstance(pub_date, date) and pub_date.tzinfo is None:
        pub_date = pub_date.replace(tzinfo=timezone.utc)
    return pub_date

def build_company_query(company: str):
    return company_keyword_query(company)

def build_industry_query(industry: str, industry_context: str, location: str):
    return industry_keyword_query(industry, industry_context, location)

def get_news(query: str, query_context: str):
    if PERPLEXITY_API_KEY is None or PERPLEXITY_API_KEY.strip() == '' or PERPLEXITY_API_KEY == 'my_perplexity_key':
        return {"results": []}

    payload = build_payload(query)
    try:
        headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
        response = requests.post(PERPLEXITY_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"payload": payload})
        return {"results": []}

def build_payload(query: str):
    return {
        "query": query,
        "max_results": MAX_RESULTS,
        "search_context_size": "medium",
        "search_after_date_filter": MIN_DATE.strftime("%m/%d/%Y"),
        "search_before_date_filter": MAX_DATE.strftime("%m/%d/%Y"),
    }
