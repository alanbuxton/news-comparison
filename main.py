from datetime import datetime, timezone, time, date
import os
import argparse
import csv
import syracuse_client
import perplexity_client
import linkup_client
import exa_client
import newsapi_client
import tavily_client
from examples import industry_location_examples, company_name_examples
from utils import MIN_DATE

# Excluding NewsAPI because it generates too much noise
CLIENTS = {"Exa": exa_client, 
           "Linkup": linkup_client, 
        #    "NewsAPI": newsapi_client, 
           "Perplexity": perplexity_client, 
           "Syracuse": syracuse_client, 
           "Tavily": tavily_client,
        }

def compare_company_results(company: str, csv_writer=None):
    """Compare company results across providers and write to CSV"""
    results_summary = []
    results_details = {}
    
    for provider, client in CLIENTS.items():
        start_time = datetime.now(tz=timezone.utc)
        arts = client.get_company_articles_for(company)
        end_time = datetime.now(tz=timezone.utc)
        duration = end_time - start_time
        arts = filter_recent_real_articles(arts)
        results_summary.append({
            'provider': provider,
            'count': len(arts),
            'duration': duration.total_seconds()
        })
        results_details[provider] = arts
    
    # Write results to CSV
    if csv_writer:
        write_articles_to_csv(csv_writer, company, None, None, results_details)
    
    return results_summary, results_details

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

def compare_industry_location_results(industry: str, location: str, csv_writer=None):
    """Compare industry/location results across providers and write to CSV"""
    results_summary = []
    results_details = {}
    
    for provider, client in CLIENTS.items():
        start_time = datetime.now(tz=timezone.utc)
        arts = client.get_industry_articles_for(industry, location)
        end_time = datetime.now(tz=timezone.utc)
        duration = end_time - start_time
        arts = filter_recent_real_articles(arts)
        results_summary.append({
            'provider': provider,
            'count': len(arts),
            'duration': duration.total_seconds()
        })
        results_details[provider] = arts
    
    # Write results to CSV
    if csv_writer:
        write_articles_to_csv(csv_writer, None, industry, location, results_details)
    
    return results_summary, results_details

def write_articles_to_csv(csv_writer, company=None, industry=None, location=None, results_details=None):
    """Write article results to CSV file"""
    for provider, articles in results_details.items():
        for article in articles:
            # Clean all text fields to remove line breaks and normalize whitespace
            def clean_text(text):
                if text and isinstance(text, str):
                    return ' '.join(text.split())
                return text
            
            row = {
                'company': company or '',
                'industry': industry or '',
                'location': location or '',
                'provider': provider,
                'headline': clean_text(article.get('headline', '')),
                'published_by': clean_text(article.get('published_by', '')),
                'published_date': article.get('published_date', ''),
                'published_date_clean': article.get('published_date_clean', ''),
                'activity_type': clean_text(article.get('activity_type', '')),
                'document_url': article.get('document_url', ''),
                'summary_text': clean_text(article.get('summary_text', ''))
            }
            csv_writer.writerow(row)

def filter_recent_real_articles(articles, min_date=MIN_DATE):
    seen_urls = set()
    min_datetime = datetime.combine(min_date, time.min)
    min_datetime = min_datetime.replace(tzinfo=timezone.utc)
    articles_to_keep = []
    for article in articles:
        # Always keep error rows
        if article.get('headline') == '*** ERROR ***':
            articles_to_keep.append(article)
            continue
            
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
        raw_date_str = f"(raw date: {art['published_date']})" if art.get('published_date') else ""
        published_by = art.get('published_by', '')
        published_date_clean = art.get('published_date_clean', 'No Date')
        output.append(f"{published_by} - {published_date_clean} {raw_date_str} {act_class_str}")
        output.append(str(art.get('document_url', '')))
        output.append(str(art.get('summary_text', '')))
        output.append("")
    return output

def print_articles(arts):
    articles_output = format_articles(arts)
    print('\n'.join(articles_output))

def run_comparison(prefix: str, output_dir: str = 'results'):
    """Run comparison and output results to CSV files"""
    # Create results directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    companies_file = os.path.join(output_dir, f"{prefix}-companies.csv")
    industries_file = os.path.join(output_dir, f"{prefix}-industries.csv")
    
    print(f"Running comparison with prefix '{prefix}'...")
    print(f"Output directory: {output_dir}")
    print()
    
    # Define CSV headers
    csv_headers = [
        'company', 'industry', 'location', 'provider', 'headline', 
        'published_by', 'published_date', 'published_date_clean', 
        'activity_type', 'document_url', 'summary_text'
    ]
    
    # Write companies results
    print("Processing companies...")
    with open(companies_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=csv_headers)
        csv_writer.writeheader()
        
        for company_name in company_name_examples:
            print(f"  - {company_name}")
            summary, details = compare_company_results(company_name, csv_writer=csv_writer)
            # Print summary to console
            summary_str = '; '.join([f"{s['provider']} got {s['count']} in {s['duration']:.2f}s" for s in summary])
            print(f"    {summary_str}")
    
    # Write industries results
    print("\nProcessing industries/locations...")
    with open(industries_file, 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.DictWriter(f, fieldnames=csv_headers)
        csv_writer.writeheader()
        
        for industry_location in industry_location_examples:
            industry = industry_location['industry']
            location = industry_location['location']
            print(f"  - {industry} - {location}")
            summary, details = compare_industry_location_results(**industry_location, csv_writer=csv_writer)
            # Print summary to console
            summary_str = '; '.join([f"{s['provider']} got {s['count']} in {s['duration']:.2f}s" for s in summary])
            print(f"    {summary_str}")
    
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
        help='Prefix for output filenames (e.g., "test_run" creates test_run-companies.csv)'
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