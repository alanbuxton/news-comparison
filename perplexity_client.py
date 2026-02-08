import requests
from utils import PERPLEXITY_API_KEY, MIN_DATE, MAX_DATE, log_error
from datetime import date, timedelta, datetime, timezone
import json

PROVIDER_NAME = "Perplexity"
PERPLEXITY_ENDPOINT = "https://api.perplexity.ai/chat/completions"

def get_industry_articles_for(industry: str, location: str):
    query_context = f"industry={industry}, location={location}"
    user_command = build_industry_user_command(industry, location)
    system_command = build_industry_system_command(industry)
    payload = build_payload(user_command, system_command)
    response = get_news(payload, query_context)
    if response:
        industry_articles = perplexity_response_to_articles(response, query_context)
        return industry_articles
    return []

def get_company_articles_for(company: str):
    query_context = f"company={company}"
    user_command = build_company_user_command(company)
    system_command = build_company_system_command(company)
    payload = build_payload(user_command, system_command)
    response = get_news(payload, query_context)
    if response:
        company_articles = perplexity_response_to_articles(response, query_context)
        return company_articles
    else:
        return []

def parse_perplexity_responses(perplexity_content: dict, query_context: str) -> list:
    articles = []
    for item in perplexity_content:
        try:
            pub_date = datetime.fromisoformat(item["published_date"])  # Needs Python 3.11 or higher to work
            if isinstance(pub_date, date) and pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=timezone.utc)
            item["published_date_clean"] = pub_date
            articles.append(item)
        except Exception as e:
            log_error(PROVIDER_NAME, "PARSE_DATE", query_context, str(e), item)
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

def perplexity_response_to_articles(response, query_context: str):
    try:
        content = response['choices'][0]['message']['content']
        perplexity_content = json.loads(content)
        articles = parse_perplexity_responses(perplexity_content, query_context)
        return articles
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_RESPONSE", query_context, str(e), response)
        return []

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

def get_news(payload: dict, query_context: str):
    if PERPLEXITY_API_KEY is None or PERPLEXITY_API_KEY.strip() == '' or PERPLEXITY_API_KEY == 'my_perplexity_key':
        return {'choices': [{"message": {"content": "[]"}}]}
    
    try:
        headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
        response = requests.post(PERPLEXITY_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        response_json = response.json()
        return response_json
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"payload": payload})
        return None

def build_payload(user_command: str, system_command: str):
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": system_command},
            {"role": "user", "content": user_command},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "schema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "headline": {"type": "string"},
                            "summary_text": {"type": "string"},
                            "published_date": {"type": "string", "format": "date-time"},
                            "published_by": {"type": "string"},
                            "document_url": {"type": "string"}
                        },
                        "required": ["headline", "summary_text", "published_date", "published_by", "document_url"]
                    }
                }
            }
        },
        "web_search_options": {
            "search_context_size": "medium"
        },
        "search_after_date_filter": MIN_DATE.strftime("%m/%d/%Y"),
        "search_before_date_filter": MAX_DATE.strftime("%m/%d/%Y"),
    }
    return payload
