from utils import NEWSAPI_API_KEY, MIN_DATE, MAX_DATE
import requests
from datetime import datetime

NEWSAPI_ENDPOINT="https://newsapi.org/v2/everything"

def call_newsapi_stories(query: str):
    if NEWSAPI_API_KEY is None or NEWSAPI_API_KEY.strip() == '' or NEWSAPI_API_KEY == 'my_syracuse_key':
        return {'articles':[]}
    params = {"q":query,
              "apiKey":NEWSAPI_API_KEY,
              # Paid plan is required for from/to
            #   "from":MIN_DATE.isoformat(), 
            #   "to":MAX_DATE.isoformat(),
              "language":"en"}
    response = requests.get(NEWSAPI_ENDPOINT, params=params)
    response.raise_for_status()
    return response.json()

def get_company_articles_for(company: str):
    resp = call_newsapi_stories(company)
    articles = parse_response(resp)
    return articles

def get_industry_articles_for(industry: str, location: str):
    resp = call_newsapi_stories(f"{industry} in {location}")
    articles = parse_response(resp)
    return articles

def parse_response(resp_json) -> list[dict]:
    try:
        return [item_to_article(x) for x in resp_json['articles']]
    except:
        print(f"Couldn't parse {resp_json}")
        raise

def item_to_article(item: dict):
    return {
        "headline": item['title'],
        "published_date_clean": datetime.fromisoformat(item["publishedAt"]),
        "published_date": item["publishedAt"],
        "summary_text": item['description'],
        "published_by": item['source']['name'],
        "document_url": item['url'],
    }
