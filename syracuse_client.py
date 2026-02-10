from utils import SYRACUSE_API_KEY, log_error
import requests
from typing import Union
from datetime import datetime
import os

PROVIDER_NAME = "Syracuse"
SYRACUSE_ENDPOINT = os.environ.get("SYRACUSE_ENDPOINT", "https://syracuse.1145.am/api/v1/stories")

def call_syracuse_activities(params: Union[dict, None], query_context: str):
    if SYRACUSE_API_KEY is None or SYRACUSE_API_KEY.strip() == '' or SYRACUSE_API_KEY == 'my_syracuse_key':
        return {'results': []}
    
    try:
        headers = {
            "Authorization": f"Token {SYRACUSE_API_KEY}"
        }
        response = requests.get(SYRACUSE_ENDPOINT, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"params": params})
        return {'results': []}

def get_company_articles_for(company: str):
    query_context = f"company={company}"
    resp = call_syracuse_activities({"org_name": company}, query_context)
    articles = parse_response(resp, query_context)
    return articles

def get_industry_articles_for(industry: str, location: str):
    query_context = f"industry={industry}, location={location}"
    resp = call_syracuse_activities({"industry": industry, "location": location}, query_context)
    articles = parse_response(resp, query_context)
    return articles

def parse_response(resp_json, query_context: str) -> list[dict]:
    try:
        articles = []
        for item in resp_json['results']:
            article = item_to_article(item, query_context)
            articles.append(article)
        return articles
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_RESPONSE", query_context, str(e), resp_json)
        return []

def item_to_article(item: dict, query_context: str):
    try:
        return {
            "headline": item['headline'],
            "published_date_clean": datetime.fromisoformat(item["date_published"]),
            "published_date": item["date_published"],
            "summary_text": item['document_extract'],
            "published_by": item['source_organization'],
            "document_url": item['document_url'],
            "activity_type": item['activity_class'],
        }
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_ARTICLE", query_context, str(e), item)
        return {
            "headline": "*** ERROR ***",
            "summary_text": str(e),
            "published_date": "",
            "published_date_clean": "",
            "published_by": "",
            "document_url": getattr(item, 'document_url', 'unknown'),
            "activity_type": ""
        }