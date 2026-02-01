import requests
from utils import PERPLEXITY_API_KEY, PERPLEXITY_ENDPOINT
from datetime import date, timedelta, datetime, timezone
import json

def get_industry_articles_for(industry: str, location: str):
    user_command = build_industry_user_command(industry, location)
    system_command = build_industry_system_command(industry)
    payload = build_payload(user_command, system_command)
    response = get_news(payload)
    industry_articles = perplexity_response_to_articles(response)
    return industry_articles

def get_company_articles_for(company: str):
    user_command = build_company_user_command(company)
    system_command = build_company_system_command(company)
    payload = build_payload(user_command, system_command)
    response = get_news(payload)
    if response:
        company_articles = perplexity_response_to_articles(response)
        return company_articles
    else:
        return []

def parse_perplexity_responses(perplexity_content: dict) -> list:
    articles = []
    for item in perplexity_content:
        try:
            pub_date = datetime.fromisoformat(item["published_date"]) # Needs Python 3.11 or higher to work
            if isinstance(pub_date, date) and pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=timezone.utc)
            item["published_date_clean"] = pub_date
            articles.append(item)
        except: # date not always in isoformat
            pass
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

def perplexity_response_to_articles(response):
    content = response['choices'][0]['message']['content']
    perplexity_content = json.loads(content)
    articles = parse_perplexity_responses(perplexity_content)
    return articles

def build_company_system_command(company: str):
    return f"You are a market research analyst with deep knowledge of {company} and its history."

def build_company_user_command(company: str):
    user_command = (
                f"I need you to find recent news articles for {company}. "
                "Focus on topics like corporate finance, partnerships, product innovations, supplier risk and regulatory changes "
                "that I can use in preparing my procurement strategy, risk management and supplier negotiations. "
                "For each source cited in your response, provide a separate summary of that source's content. "
                "Prioritise more recent news articles. "
                "Please output a list of JSON objects with one JSON object per source with the following fields: "
                "headline, summary_text, published_date, published_by, document_url"
            )
    return user_command

def build_industry_system_command(industry: str):
    return f"You are a market research analyst with deep knowledge of what a procurement category manager in the {industry} industry needs."

def build_industry_user_command(industry: str, location: str):
    user_command = (
                f"I need you to produce a list of suppliers for industry: {industry} in location: {location}. Then find recent news articles for these suppliers. "
                "Focus on topics like corporate finance, partnerships, product innovations, supplier risk and regulatory changes "
                "that I can use in preparing my procurement strategy, risk management and supplier negotiations. "
                "For each source cited in your response, provide a separate summary of that source's content. "
                "Prioritise more recent news articles. "
                "Please output a list of JSON objects with one JSON object per source with the following fields: "
                "headline, summary_text, published_date, published_by, document_url"
            )
    return user_command

def get_news(payload: dict):
    if PERPLEXITY_API_KEY is None or PERPLEXITY_API_KEY.strip() == '' or PERPLEXITY_API_KEY == 'my_perplexity_key':
        return {'choices':[{"message": {"content": "[]"}}]}
    headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
    response = requests.post(PERPLEXITY_ENDPOINT, headers=headers, json=payload)
    try:
        response_json = response.json()
        return response_json
    except:
        print(f"error parsing {response}")
        return None


def build_payload(user_command :str, system_command: str, date_to :date = None, date_from :date = None):
    if date_to is None:
        date_to = date.today()
    if date_from is None:
        date_from = date_to - timedelta(days=90)

    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": system_command},
            {"role": "user", "content": user_command },
        ],
        "response_format": { "type": "json_schema",
                            "json_schema": {
                                "schema": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "headline": { "type": "string" },
                                            "summary_text": { "type": "string" },
                                            "published_date": { "type": "string", "format": "date-time" },
                                            "published_by": { "type": "string" },
                                            "document_url": { "type": "string" }
                                        },
                                        "required": ["headline", "summary_text", "published_date", "published_by", "document_url"]
                                    }
                                }
                            }
                            } ,
        "web_search_options": {
            "search_context_size": "medium"
        },
        "search_after_date_filter": date_from.strftime("%m/%d/%Y"),
        "search_before_date_filter": date_to.strftime("%m/%d/%Y"),
    }
    return payload
