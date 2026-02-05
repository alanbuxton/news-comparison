from datetime import datetime, timezone, time, date
import syracuse_client
import perplexity_client
import linkup_client
import exa_client
import newsapi_client
import tavily_client
from examples import industry_location_examples, company_name_examples
from utils import MIN_DATE

CLIENTS = {"Exa": exa_client, "Linkup": linkup_client, "NewsAPI": newsapi_client, "Perplexity": perplexity_client, 
           "Syracuse": syracuse_client, "Tavily": tavily_client}

def compare_company_results(company: str):
    print("-" * 40)
    print(f"--- {company}")
    print("-" * 40)
    results_summary = []
    results_details = {}
    for provider, client in CLIENTS.items():
        start_time = datetime.now(tz=timezone.utc)
        arts = client.get_company_articles_for(company)
        end_time = datetime.now(tz=timezone.utc)
        duration = end_time - start_time
        arts = filter_recent_real_articles(arts)
        stats = f"{provider} got {len(arts)} in {duration}"
        results_summary.append(stats)
        results_details[provider] = arts
    print_comparison(results_summary, results_details)

def print_comparison(results_summary, results_details):
    print(f"***** {'; '.join(results_summary)} *****")
    print()
    for provider, results in results_details.items():
        print("*" * 20)
        print(f"*** {provider}")
        print("*" * 20)
        print_articles(results)
        print()

def compare_industry_location_results(industry: str, location: str):
    print("-" * 40)
    print(f"--- {industry} - {location}")
    print("-" * 40)

    results_summary = []
    results_details = {}
    for provider, client in CLIENTS.items():
        start_time = datetime.now(tz=timezone.utc)
        arts = client.get_industry_articles_for(industry, location)
        end_time = datetime.now(tz=timezone.utc)
        duration = end_time - start_time
        arts = filter_recent_real_articles(arts)
        stats = f"{provider} got {len(arts)} in {duration}"
        results_summary.append(stats)
        results_details[provider] = arts
    print_comparison(results_summary, results_details)

def filter_recent_real_articles(articles, min_date=MIN_DATE):
    seen_urls = set()
    min_datetime = datetime.combine(min_date, time.min)
    min_datetime = min_datetime.replace(tzinfo=timezone.utc)
    articles_to_keep = []
    for article in articles:
        if isinstance(article['published_date_clean'], date) and article['published_date_clean'] < min_datetime:
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
    for art in sorted(arts, key=lambda x: x['published_date'], reverse=True):
        print(art['headline'])
        act_class_str = f" - {art['activity_type']}" if art.get('activity_type') else ''
        raw_date_str = f"(raw date: {art['published_date']})" if art['published_date'] else ''
        print(f"{art['published_by']} - {art['published_date_clean']}{raw_date_str}{act_class_str}")
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
