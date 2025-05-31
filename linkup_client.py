from linkup import LinkupClient
from utils import LINKUP_API_KEY
import json
from datetime import datetime, timezone

def get_industry_articles_for(industry: str, location: str):
    query = industry_query(industry, location)
    results = do_query(query)
    articles = []
    for item in results['articles']:
        article = item_to_article(item)
        if article is not None:
            articles.append(article)
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

def get_company_articles_for(company: str):
    query = company_query(company)
    results = do_query(query)
    articles = []
    for item in results['articles']:
        article = item_to_article(item)
        if article is not None:
            articles.append(article)
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

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

def industry_query(industry, location):
    prompt = (f"Fetch 10 recent news related to the {industry} industry in {location}.\n"
    "Focus on:\n"
    "- Market trends and macroeconomic developments\n"
    "- Regulatory or policy updates\n"
    "- Major deals, innovations, or disruptions\n"
    "- Any mention of key players in the space\n\n"
    "Return source titles, publication dates, and a short summary for each news item.\n\n"
    "Only include content from credible business, trade, specialized or regional news sources."
    )
    return prompt

def company_query(company_name):
    prompt = (f"Find 10 recent news mentioning {company_name}.\n\n"
    "Prioritize:\n- Product launches, strategic moves, M&A activity\n- Financial performance or investment news\n"
    "- Regulatory issues or market positioning updates\n- Regional relevance or expansion activities\n\n"
    "Summarize each relevant article in 2-3 sentences, including source, date, and URL.\n"
    "Only include information from trustworthy business or industry-specific media outlets.\n"
    )
    return prompt

def do_query(query):
    if LINKUP_API_KEY is None or LINKUP_API_KEY.strip() == '' or LINKUP_API_KEY == 'my_linkup_key':
        return {'articles':[]}
    client = LinkupClient(api_key=LINKUP_API_KEY)
    response = client.search(query=query,
        depth="standard",
        output_type="structured",
        structured_output_schema=output_schema(),
        include_images=False,
        )
    return response

def item_to_article(item: dict):
    try:
        pub_date = datetime.fromisoformat(item['publication_date'])
        pub_date = pub_date.replace(tzinfo=timezone.utc)
        return {
            "headline": item['headline'],
            "published_date": pub_date,
            "summary_text": item['summary'],
            "published_by": item['source'],
            "document_url": item['url'],
        }
    except: # date not always in iso format
        return None
