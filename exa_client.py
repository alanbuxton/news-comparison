from utils import EXA_API_KEY, MIN_DATE, MAX_DATE
from datetime import datetime
from exa_py import Exa
from urllib.parse import urlparse

def get_industry_articles_for(industry: str, location: str):
    query = industry_query(industry, location)
    resp = do_query(query)
    articles = []
    if resp is None: 
        return articles
    for item in resp.results:
        article = item_to_article(item)
        if article is not None:
            articles.append(article)
    return sorted(articles, key=lambda x: x["published_date"], reverse=True)

def get_company_articles_for(company: str):
    query = company_query(company)
    resp = do_query(query)
    articles = []
    if resp is None:
        return articles
    for item in resp.results:
        article = item_to_article(item)
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

def do_query(query):
    if EXA_API_KEY is None or EXA_API_KEY.strip() == '' or EXA_API_KEY == 'my_exa_key':
        return None
    
    client = Exa(EXA_API_KEY)
    response = client.search(query,
        end_published_date = MAX_DATE.isoformat(),
        start_published_date = MIN_DATE.isoformat(),
        type = "auto",
        contents = {
          "highlights": True
        }
        )
    return response

def item_to_article(item):
    try:
        pub_date = datetime.fromisoformat(item.published_date)
        parsed_url = urlparse(item.url)
        top_highlight = item.highlights[0] if len(item.highlights) > 0 else ""
        top_highlight = top_highlight.replace("\n"," ")
        author_string = f" ({item.author})" if item.author else ""
        return {
            "headline": item.title,
            "published_date_clean": pub_date,
            "published_date": item.published_date,
            "summary_text": top_highlight,
            "published_by": f"{parsed_url.netloc}{author_string}",
            "document_url": item.url,
        }
    except: 
        print(f"error parsing {item}")
        return None
