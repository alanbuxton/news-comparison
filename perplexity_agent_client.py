"""Perplexity Agent API client (POST /v1/agent).

Replaces the Sonar (/chat/completions) client, which Perplexity retires on
2026-09-27. Sonar tiers map onto Agent presets; sonar-pro is the `low` preset.

Unlike Sonar this endpoint rejects `search_after_date_filter` /
`search_before_date_filter` outright ("unknown field"), so the 90-day window can
only be requested in the prompt and is enforced for real by
`filter_recent_real_articles` in main.py.

Like Sonar, this asks the model to synthesise a list of articles rather than
returning the raw retrieved pages — the Agent response also carries
`search_results` blocks, but reading those would duplicate what
perplexity_search_client.py already measures. Keeping the synthesis path is also
what makes hallucinated URLs visible, which is a defect this benchmark exists to
detect: no cross-checking of returned URLs against the retrieved set is done on
purpose.
"""

import requests
from utils import PERPLEXITY_API_KEY, MIN_DATE, MAX_DATE, log_error
from queries import company_prose_query, industry_prose_query, industry_str
from datetime import date, datetime, timezone
import json

PROVIDER_NAME = "Perplexity Agent"
PERPLEXITY_ENDPOINT = "https://api.perplexity.ai/v1/agent"
PRESET = "low"      # sonar-pro equivalent; fast | low | medium | high, see https://docs.perplexity.ai/docs/agent-api/presets
TIMEOUT_SECONDS = 300   # agent runs are multi-step and take ~30s+

ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "headline": {"type": "string"},
                    "summary_text": {"type": "string"},
                    "published_date": {"type": "string"},
                    "published_by": {"type": "string"},
                    "document_url": {"type": "string"},
                },
                "required": [
                    "headline", "summary_text", "published_date",
                    "published_by", "document_url",
                ],
                "additionalProperties": False,
            },
        }
    },
    "required": ["items"],
    "additionalProperties": False,
}


def get_industry_articles_for(industry: str, industry_context: str, location: str):
    query_context = f"industry={industry}, industry_context={industry_context} location={location}"
    payload = build_payload(
        build_industry_user_command(industry, industry_context, location),
        build_industry_system_command(industry, industry_context),
    )
    response = get_news(payload, query_context)
    if response:
        return perplexity_response_to_articles(response, query_context)
    return []


def get_company_articles_for(company: str):
    query_context = f"company={company}"
    payload = build_payload(
        build_company_user_command(company),
        build_company_system_command(company),
    )
    response = get_news(payload, query_context)
    if response:
        return perplexity_response_to_articles(response, query_context)
    return []


def parse_perplexity_responses(perplexity_content: list, query_context: str) -> list:
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
            # Add error to CSV output
            articles.append({
                "headline": "*** ERROR ***",
                "summary_text": str(e),
                "published_date": "",
                "published_date_clean": "",
                "published_by": "",
                "document_url": item.get('document_url', 'unknown'),
            })
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)


def extract_message_text(response: dict) -> str:
    """The Agent response is an `output` array with one item per step taken —
    several `search_results` blocks then the final `message`. Only the message
    carries the structured answer."""
    for item in reversed(response.get("output", [])):
        if item.get("type") == "message":
            return "".join(
                part.get("text", "") for part in item.get("content", [])
            )
    raise ValueError("no message item in agent output")


def perplexity_response_to_articles(response, query_context: str):
    try:
        content = extract_message_text(response)
        perplexity_content = json.loads(content)["items"]
        return parse_perplexity_responses(perplexity_content, query_context)
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_RESPONSE", query_context, str(e), response)
        return []


def build_date_window_instruction():
    """Every other provider gets the 90-day window as a server-side filter.
    /v1/agent rejects those parameters, so it is asked for in the prompt — this
    compensates for an API limitation rather than giving the Agent a different
    question."""
    return (
        f"Only include articles published between {MIN_DATE.date().isoformat()} and "
        f"{MAX_DATE.date().isoformat()}. Do not include anything published outside "
        "that window."
    )


# Output shape is an API constraint, not part of the question being asked, so it
# lives here rather than in queries.py.
OUTPUT_INSTRUCTION = (
    "Return one object per source with the following fields: headline, "
    "summary_text, published_date, published_by, document_url. published_date "
    "must be an ISO 8601 date. published_by must be the name of the publication "
    "that published the article."
)


def build_company_system_command(company: str):
    return f"You are a market research analyst with deep knowledge of {company} and its history."


def build_company_user_command(company: str):
    return "\n".join([
        company_prose_query(company),
        build_date_window_instruction(),
        OUTPUT_INSTRUCTION,
    ])


def build_industry_system_command(industry: str, industry_context: str):
    return (
        "You are a market research analyst with deep knowledge of what a procurement "
        f"category manager in the {industry_str(industry, industry_context)} industry needs."
    )


def build_industry_user_command(industry: str, industry_context: str, location: str):
    return "\n".join([
        industry_prose_query(industry, industry_context, location),
        build_date_window_instruction(),
        OUTPUT_INSTRUCTION,
    ])


def get_news(payload: dict, query_context: str):
    if PERPLEXITY_API_KEY is None or PERPLEXITY_API_KEY.strip() == '' or PERPLEXITY_API_KEY == 'my_perplexity_key':
        return None

    try:
        headers = {"Authorization": f"Bearer {PERPLEXITY_API_KEY}"}
        response = requests.post(
            PERPLEXITY_ENDPOINT, headers=headers, json=payload, timeout=TIMEOUT_SECONDS
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"payload": payload})
        return None


def build_payload(user_command: str, system_command: str):
    return {
        "preset": PRESET,
        "instructions": system_command,
        "input": user_command,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "articles",
                "schema": ARTICLE_SCHEMA,
            }
        },
    }
