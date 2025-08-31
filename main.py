from datetime import datetime, timezone, time
import syracuse_client
import perplexity_client
import linkup_client
from examples import industry_location_examples, company_name_examples
from utils import MIN_DATE

def compare_company_results(company: str):
    print("-" * 40)
    print(f"--- {company}")
    print("-" * 40)
    t1 = datetime.now(tz=timezone.utc)
    p_arts = perplexity_client.get_company_articles_for(company)
    t2 = datetime.now(tz=timezone.utc)
    s_arts = syracuse_client.get_company_articles_for(company)
    t3 = datetime.now(tz=timezone.utc)
    l_arts = linkup_client.get_company_articles_for(company)
    t4 = datetime.now(tz=timezone.utc)
    p_arts = filter_recent_real_articles(p_arts)
    s_arts = filter_recent_real_articles(s_arts)
    l_arts = filter_recent_real_articles(l_arts)
    print_comparison(p_arts, s_arts, l_arts, t1, t2, t3, t4)

def print_comparison(p_arts, s_arts, l_arts, t1, t2, t3, t4):
    print(f"***** Perplexity got {len(p_arts)} in {t2-t1}; Syracuse got {len(s_arts)} in {t3-t2}: Linkup got {len(l_arts)} in {t4-t3} *****")
    print("*" * 20)
    print("*** Perplexity")
    print("*" * 20)
    print_articles(p_arts)
    print("*" * 20)
    print("Syracuse")
    print("*" * 20)
    print_articles(s_arts)
    print("*" * 20)
    print("LinkUp")
    print("*" * 20)
    print_articles(l_arts)
    print()

def compare_industry_location_results(industry: str, location: str):
    print("-" * 40)
    print(f"--- {industry} - {location}")
    print("-" * 40)
    t1 = datetime.now(tz=timezone.utc)
    p_arts = perplexity_client.get_industry_articles_for(industry, location)
    t2 = datetime.now(tz=timezone.utc)
    s_arts = syracuse_client.get_industry_articles_for(industry, location)
    t3 = datetime.now(tz=timezone.utc)
    l_arts = linkup_client.get_industry_articles_for(industry, location)
    t4 = datetime.now(tz=timezone.utc)
    p_arts = filter_recent_real_articles(p_arts)
    s_arts = filter_recent_real_articles(s_arts)
    l_arts = filter_recent_real_articles(l_arts)
    print_comparison(p_arts, s_arts, l_arts, t1, t2, t3, t4)

def filter_recent_real_articles(articles, min_date=MIN_DATE):
    seen_urls = set()
    min_datetime = datetime.combine(min_date, time.min)
    min_datetime = min_datetime.replace(tzinfo=timezone.utc)
    articles_to_keep = []
    for article in articles:
        if article['published_date'] < min_datetime:
            continue
        if article['document_url'] is None:
            continue
        if not article['document_url'].lower().startswith("http"):
            continue
        if article['document_url'] in seen_urls:
            continue
        articles_to_keep.append(article)
        seen_urls.add(article['document_url'])
    return articles_to_keep

def print_articles(arts):
    for art in arts:
        print(art['headline'])
        act_class_str = f" - {art['activity_type']}" if art.get('activity_type') else ''
        print(f"{art['published_by']} - {art['published_date']} {act_class_str}")
        print(art['document_url'])
        print(art['summary_text'])
        print()

if __name__ == '__main__':
    print()
    print("*" * 50)
    print("*** COMPANIES")
    print("*" * 50)
    print()
    for company_name in company_name_examples:
        compare_company_results(company_name)
    print()
    print("*" * 50)
    print("*** INDUSTRY / LOCATIONS")
    print("*" * 50)
    print()
    for industry_location in industry_location_examples:
        compare_industry_location_results(**industry_location)
