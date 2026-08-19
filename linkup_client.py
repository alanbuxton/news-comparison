from linkup import LinkupClient
from utils import LINKUP_API_KEY, MAX_DATE, MIN_DATE, log_error
from queries import company_prose_query, industry_prose_query
import json
from datetime import datetime, timezone

PROVIDER_NAME = "Linkup"

def get_industry_articles_for(industry: str, industry_str: str, location: str):
    query = industry_query(industry, industry_str, location)
    query_context = f"industry={industry}, industry_str={industry_str}, location={location}"
    results = do_query(query, query_context)
    articles = []
    for item in results['articles']:
        article = item_to_article(item, query_context)
        articles.append(article)
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def get_company_articles_for(company: str):
    query = company_query(company)
    query_context = f"company={company}"
    results = do_query(query, query_context)
    articles = []
    for item in results['articles']:
        article = item_to_article(item, query_context)
        articles.append(article)
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def output_schema():
    schema = {
        "type": "object",
        "properties": {
            "articles": {
                "type": "array",
                "description": "List of news articles related to the specified company or industry.",
                "items": {
                    "type": "object",
                    "properties": {
                        "headline": {
                            "type": "string",
                            "description": "Title of the news article"
                        },
                        "publication_date": {
                            "type": "string",
                            "description": "Date when the article was published",
                            "format": "date-time"
                        },
                        "summary": {
                            "type": "string",
                            "description": "Brief summary of the article (max 3 lines)"
                        },
                        "source": {
                            "type": "string",
                            "description": "News source or publication name"
                        },
                        "url": {
                            "type": "string",
                            "description": "Link to the original article"
                        }
                    },
                    "required": ["headline", "publication_date", "source", "url"]
                }
            }
        },
        "required": ["articles"]
    }
    return json.dumps(schema)

OUTPUT_INSTRUCTION = (
    "Return the source title, publication date, publication name and URL for "
    "each news item, with a summary of 2-3 sentences."
)

def industry_query(industry, industry_context, location):
    return f"{industry_prose_query(industry, industry_context, location)}\n{OUTPUT_INSTRUCTION}"

def company_query(company_name):
    return f"{company_prose_query(company_name)}\n{OUTPUT_INSTRUCTION}"

def do_query(query, query_context: str):
    if LINKUP_API_KEY is None or LINKUP_API_KEY.strip() == '' or LINKUP_API_KEY == 'my_linkup_key':
        return {'articles': []}
    
    try:
        client = LinkupClient(api_key=LINKUP_API_KEY)
        response = client.search(query=query,
            depth="deep",
            output_type="structured",
            structured_output_schema=output_schema(),
            include_images=False,
            from_date=MIN_DATE,
            to_date=MAX_DATE,
        )
        return response
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"query": query[:400]})
        return {'articles': []}

def item_to_article(item: dict, query_context: str):
    try:
        pub_date = datetime.fromisoformat(item['publication_date'])
        pub_date = pub_date.replace(tzinfo=timezone.utc)
        return {
            "headline": item['headline'],
            "published_date_clean": pub_date,
            "published_date": item["publication_date"],
            "summary_text": item.get('summary', ''),
            "published_by": item['source'],
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