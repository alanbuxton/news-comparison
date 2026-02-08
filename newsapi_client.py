from utils import NEWSAPI_API_KEY, MIN_DATE, MAX_DATE, log_error
import requests
from datetime import datetime

PROVIDER_NAME = "NewsAPI"
NEWSAPI_ENDPOINT = "https://newsapi.org/v2/everything"

def call_newsapi_stories(query: str, query_context: str):
    if NEWSAPI_API_KEY is None or NEWSAPI_API_KEY.strip() == '' or NEWSAPI_API_KEY == 'my_newsapi_key':
        return {'articles': []}
    
    try:
        params = {
            "q": query,
            "apiKey": NEWSAPI_API_KEY,
            # Paid plan is required for from/to
            # "from": MIN_DATE.isoformat(), 
            # "to": MAX_DATE.isoformat(),
            "language": "en"
        }
        response = requests.get(NEWSAPI_ENDPOINT, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"query": query})
        return {'articles': []}

def get_company_articles_for(company: str):
    query_context = f"company={company}"
    resp = call_newsapi_stories(company, query_context)
    articles = parse_response(resp, query_context)
    return articles

def get_industry_articles_for(industry: str, location: str):
    query_context = f"industry={industry}, location={location}"
    resp = call_newsapi_stories(f"{industry} in {location}", query_context)
    articles = parse_response(resp, query_context)
    return articles

def parse_response(resp_json, query_context: str) -> list[dict]:
    try:
        articles = []
        for item in resp_json['articles']:
            article = item_to_article(item, query_context)
            if article is not None:
                articles.append(article)
        return articles
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_RESPONSE", query_context, str(e), resp_json)
        return []

def item_to_article(item: dict, query_context: str):
    try:
        return {
            "headline": item['title'],
            "published_date_clean": datetime.fromisoformat(item["publishedAt"]),
            "published_date": item["publishedAt"],
            "summary_text": item.get('description', ''),
            "published_by": item['source']['name'],
            "document_url": item['url'],
        }
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_ARTICLE", query_context, str(e), item)
        return None
