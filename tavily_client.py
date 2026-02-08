from tavily import TavilyClient
from utils import TAVILY_API_KEY, MAX_DATE, MIN_DATE, log_error
import json
from datetime import datetime, timezone

PROVIDER_NAME = "Tavily"

def get_industry_articles_for(industry: str, location: str):
    query = industry_query(industry, location)
    query_context = f"industry={industry}, location={location}"
    results = do_query(query, query_context)
    articles = []
    for item in results['results']:
        article = item_to_article(item, query_context)
        if article is not None:
            articles.append(article)
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

def get_company_articles_for(company: str):
    query = company_query(company)
    query_context = f"company={company}"
    results = do_query(query, query_context)
    articles = []
    for item in results['results']:
        article = item_to_article(item, query_context)
        if article is not None:
            articles.append(article)
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

def industry_query(industry, location):
    prompt = (f"Fetch recent news related to the {industry} industry in {location}.\n"
    "Focus on:\n"
    "- Market trends and macroeconomic developments\n"
    "- Regulatory or policy updates\n"
    "- Major deals, innovations, or disruptions\n"
    "- Any mention of key players in the space\n\n"
    "Only include content from credible business, trade, specialized or regional news sources."
    )
    return prompt

def company_query(company_name):
    prompt = (f"Find recent news mentioning {company_name}.\n\n"
    "Prioritize:\n- Product launches, strategic moves, M&A activity\n- Financial performance or investment news\n"
    "- Regulatory issues or market positioning updates\n- Regional relevance or expansion activities\n\n"
    "Only include information from trustworthy business or industry-specific media outlets."
    )
    return prompt

def do_query(query, query_context):
    if TAVILY_API_KEY is None or TAVILY_API_KEY.strip() == '' or TAVILY_API_KEY == 'my_tavily_key':
        return {'results':[]}
    
    try:
        client = TavilyClient(api_key=TAVILY_API_KEY)
        response = client.search(query=query[:400],
            search_depth="advanced",
            max_results=100,
            topic="news",
            start_date=MIN_DATE.date().isoformat(),
            end_date=MAX_DATE.date().isoformat(),
            )
        return response
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"query": query[:400]})
        return {'results': []}

def item_to_article(item: dict, query_context: str):
    try:
        return {
            "headline": item['title'],
            "published_date_clean": "",
            "published_date": "",
            "summary_text": item['content'].replace("\n"," ")[:1000],
            "published_by": "",
            "document_url": item['url'],
        }
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_ARTICLE", query_context, str(e), item)
        return None