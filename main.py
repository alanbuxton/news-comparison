from datetime import datetime, timezone, time, date
import os
import argparse
import syracuse_client
import perplexity_client
import linkup_client
import exa_client
import newsapi_client
import tavily_client
from examples import industry_location_examples, company_name_examples
from utils import MIN_DATE

CLIENTS = {"Exa": exa_client, "Linkup": linkup_client, 
           "NewsAPI": newsapi_client, 
           "Perplexity": perplexity_client, 
           "Syracuse": syracuse_client, "Tavily": tavily_client}

def compare_company_results(company: str, output_file=None):
    output = []
    output.append("-" * 40)
    output.append(f"--- {company}")
    output.append("-" * 40)
    
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
    
    comparison_output = format_comparison(results_summary, results_details)
    output.extend(comparison_output)
    
    result_text = '\n'.join(output)
    if output_file:
        output_file.write(result_text + '\n')
    else:
        print(result_text)

def format_comparison(results_summary, results_details):
    output = []
    output.append(f"***** {'; '.join(results_summary)} *****")
    output.append("")
    
    for provider, results in results_details.items():
        output.append("*" * 20)
        output.append(f"*** {provider}")
        output.append("*" * 20)
        output.extend(format_articles(results))
        output.append("")
    
    return output

def print_comparison(results_summary, results_details):
    comparison_output = format_comparison(results_summary, results_details)
    print('\n'.join(comparison_output))

def compare_industry_location_results(industry: str, location: str, output_file=None):
    output = []
    output.append("-" * 40)
    output.append(f"--- {industry} - {location}")
    output.append("-" * 40)

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
    
    comparison_output = format_comparison(results_summary, results_details)
    output.extend(comparison_output)
    
    result_text = '\n'.join(output)
    if output_file:
        output_file.write(result_text + '\n')
    else:
        print(result_text)

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

def format_articles(arts):
    output = []
    for art in sorted(arts, key=lambda x: x['published_date'], reverse=True):
        output.append(str(art.get('headline', '')))
        act_class_str = f" - {art['activity_type']}" if art.get('activity_type') else ''
        raw_date_str = f"(raw date: {art['published_date']})" if art.get('published_date') else ''
        published_by = art.get('published_by', '')
        published_date_clean = art.get('published_date_clean', '')
        output.append(f"{published_by} - {published_date_clean}{raw_date_str}{act_class_str}")
        output.append(str(art.get('document_url', '')))
        output.append(str(art.get('summary_text', '')))
        output.append("")
    return output

def print_articles(arts):
    articles_output = format_articles(arts)
    print('\n'.join(articles_output))

def run_comparison(prefix: str, output_dir: str = 'results'):
    # Create results directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    companies_file = os.path.join(output_dir, f"{prefix}-companies.txt")
    industries_file = os.path.join(output_dir, f"{prefix}-industries.txt")
    
    print(f"Running comparison with prefix '{prefix}'...")
    print(f"Output directory: {output_dir}")
    print()
    
    # Write companies results
    print("Processing companies...")
    with open(companies_file, 'w') as f:
        f.write("*" * 50 + "\n")
        f.write("*** COMPANIES\n")
        f.write("*" * 50 + "\n")
        f.write("\n")
        
        for company_name in company_name_examples:
            compare_company_results(company_name, output_file=f)
    
    # Write industries results
    print("Processing industries/locations...")
    with open(industries_file, 'w') as f:
        f.write("*" * 50 + "\n")
        f.write("*** INDUSTRY / LOCATIONS\n")
        f.write("*" * 50 + "\n")
        f.write("\n")
        
        for industry_location in industry_location_examples:
            compare_industry_location_results(**industry_location, output_file=f)
    
    print()
    print("✓ Results written to:")
    print(f"  - {companies_file}")
    print(f"  - {industries_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Compare news article results across multiple providers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s test_run
  %(prog)s benchmark --output-dir ./output
  %(prog)s daily_check -o ./daily_results
        """
    )
    
    parser.add_argument(
        'prefix',
        type=str,
        help='Prefix for output filenames (e.g., "test_run" creates test_run-companies.txt)'
    )
    
    parser.add_argument(
        '-o', '--output-dir',
        type=str,
        default='results',
        help='Directory to write output files (default: results)'
    )
    
    args = parser.parse_args()
    
    run_comparison(args.prefix, args.output_dir)

if __name__ == '__main__':
    main()