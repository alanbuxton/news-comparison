from utils import EXA_API_KEY, MIN_DATE, MAX_DATE, log_error
from datetime import datetime
from exa_py import Exa
from queries import company_keyword_query, industry_keyword_query

PROVIDER_NAME = "Exa"

def get_industry_articles_for(industry: str, industry_context: str, location: str):
    query = industry_query(industry, industry_context, location)
    query_context = f"industry={industry}, industry_context={industry_context}, location={location}"
    resp = do_query(query, query_context)
    articles = []
    if resp is None: 
        return articles
    for item in resp.results:
        article = item_to_article(item, query_context)
        articles.append(article)
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def get_company_articles_for(company: str):
    query = company_query(company)
    query_context = f"company={company}"
    resp = do_query(query, query_context)
    articles = []
    if resp is None:
        return articles
    for item in resp.results:
        article = item_to_article(item, query_context)
        articles.append(article)
    return sorted(articles, key=lambda x: x.get("published_date", ""), reverse=True)

def industry_query(industry, industry_context, location):
    return industry_keyword_query(industry, industry_context, location)

def company_query(company_name):
    return company_keyword_query(company_name)

def do_query(query, query_context: str):
    if EXA_API_KEY is None or EXA_API_KEY.strip() == '' or EXA_API_KEY == 'my_exa_key':
        return None
    
    try:
        client = Exa(EXA_API_KEY)
        response = client.search(query,
            end_published_date=MAX_DATE.isoformat(),
            start_published_date=MIN_DATE.isoformat(),
            category="news",
            num_results=20,
            type="auto",
            contents={
                "highlights": True
            }
        )
        return response
    except Exception as e:
        log_error(PROVIDER_NAME, "API_QUERY", query_context, str(e), {"query": query[:400]})
        return None

def item_to_article(item, query_context: str):
    try:
        pub_date = datetime.fromisoformat(item.published_date)
        top_highlight = item.highlights[0] if len(item.highlights) > 0 else ""
        top_highlight = top_highlight.replace("\n", " ")
        return {
            "headline": item.title,
            "published_date_clean": pub_date,
            "published_date": item.published_date,
            "summary_text": top_highlight,
            # Exa returns no publisher name. `item.author` is not one — it is
            # sometimes a journalist, sometimes a publication — so it is not
            # used here. The domain is derived centrally in main.py instead.
            "published_by": "",
            "document_url": item.url,
            # Recorded as supplied, like published_by. Exa returns None under
            # type="auto"; under type="neural" it returns 1 - i/(n-1), a rank
            # ramp identical for every query, so it carries no quality signal.
            # That absence is reported by analyse.py rather than papered over.
            "relevance_score": getattr(item, "score", None),
        }
    except Exception as e:
        log_error(PROVIDER_NAME, "PARSE_ARTICLE", query_context, str(e), {
            "url": getattr(item, 'url', 'unknown'),
            "title": getattr(item, 'title', 'unknown'),
            "published_date": getattr(item, 'published_date', 'unknown'),
            "author": getattr(item, 'author', None),
            "highlights": getattr(item, 'highlights', []),
        })
        return {
            "headline": "*** ERROR ***",
            "summary_text": str(e),
            "published_date": "",
            "published_date_clean": "",
            "published_by": "",
            "document_url": getattr(item, 'url', 'unknown'),
        }