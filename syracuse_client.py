from utils import SYRACUSE_API_KEY
import requests
from typing import Union
from datetime import datetime

SYRACUSE_ENDPOINT="https://syracuse.1145.am/api/v1/stories"

def call_syracuse_activities(params: Union[dict,None]):
    if SYRACUSE_API_KEY is None or SYRACUSE_API_KEY.strip() == '' or SYRACUSE_API_KEY == 'my_syracuse_key':
        return {'results':[]}
    headers = {
        "Authorization": f"Token {SYRACUSE_API_KEY}"
    }
    response = requests.get(SYRACUSE_ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def get_company_articles_for(company: str):
    resp = call_syracuse_activities({"org_name":company})
    articles = parse_response(resp)
    return articles

def get_industry_articles_for(industry: str, location: str):
    resp = call_syracuse_activities({"industry":industry, "location":location})
    articles = parse_response(resp)
    return articles

def parse_response(resp_json) -> list[dict]:
    try:
        return [item_to_article(x) for x in resp_json['results']]
    except:
        print(f"Couldn't parse {resp_json}")
        raise

def item_to_article(item: dict):
    return {
        "headline": item['headline'],
        "published_date_clean": datetime.fromisoformat(item["date_published"]),
        "published_date": item["date_published"],
        "summary_text": item['document_extract'],
        "published_by": item['source_organization'],
        "document_url": item['document_url'],
        "activity_type": item['activity_class'],
    }
