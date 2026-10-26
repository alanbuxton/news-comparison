import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from email.utils import parsedate_to_datetime
from urllib.parse import urlparse
import json

load_dotenv()

PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
SYRACUSE_API_KEY = os.environ.get('SYRACUSE_API_KEY')
LINKUP_API_KEY = os.environ.get('LINKUP_API_KEY')
EXA_API_KEY = os.environ.get('EXA_API_KEY')
NEWSAPI_API_KEY = os.environ.get('NEWSAPI_API_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
MAX_DATE = datetime.now(tz=timezone.utc)
MIN_DATE = MAX_DATE - timedelta(days=90)
ERROR_LOG_DIR = "results/errors"

def publisher_domain(url: str) -> str:
    """Hostname of an article URL, minus any leading "www.".

    Derived centrally for every provider so no provider is credited or
    penalised for a publisher name its API never actually returned. Scoring
    runs on the provider-supplied `published_by`; this is the weaker fallback
    shown alongside it, since a domain is usually enough to judge credibility.
    """
    if not url:
        return ""
    try:
        netloc = urlparse(url).netloc.lower()
    except Exception:
        return ""
    return netloc[4:] if netloc.startswith("www.") else netloc


# Formats seen from providers whose dates are written by an LLM (Linkup, the
# Perplexity Agent): "October 7, 2026", "7 October 2026", "Oct 7, 2026".
_LOOSE_DATE_FORMATS = ("%B %d, %Y", "%d %B %Y", "%b %d, %Y", "%d %b %Y", "%b. %d, %Y")


def parse_loose_date(raw: str) -> datetime | None:
    """Parse a provider's date string: ISO 8601, RFC 2822 or a written-out full
    date. Returns None for anything else, including partial dates ("2026-08")
    and prose ("Not stated in the supplied source").

    Callers must keep the article with a blank date rather than turn it into an
    error row: an unreadable date is a metadata failure, scored on the metadata
    axis, not an API failure. Linkup's errors in the 2026-10-25 run were all
    this (319 articles) and wrongly drove its trust cap.
    """
    raw = (raw or "").strip()
    if not raw:
        return None
    parsers = [datetime.fromisoformat, parsedate_to_datetime] + [
        (lambda s, f=f: datetime.strptime(s, f)) for f in _LOOSE_DATE_FORMATS
    ]
    for parser in parsers:
        try:
            parsed = parser(raw)
        except Exception:
            continue
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    return None


def set_error_log_dir(dir_path: str):
    global ERROR_LOG_DIR
    ERROR_LOG_DIR = dir_path

def log_error(provider: str, error_type: str, query_context: str, error_message: str, data: dict = None):
    """
    Log errors to a file organized by provider and date.

    Args:
        provider: Name of the provider (e.g., "Tavily", "Exa")
        error_type: Type of error (e.g., "API_QUERY", "PARSE_ARTICLE")
        query_context: Context of the query (e.g., "company=Apple" or "industry=Tech, location=US")
        error_message: The actual error message
        data: Optional additional data to log (will be JSON serialized)
    """
    os.makedirs(ERROR_LOG_DIR, exist_ok=True)

    timestamp = datetime.now(tz=timezone.utc)
    time_str = timestamp.strftime("%H:%M:%S")

    # Create filename: {run_dir}/errors/{Provider}.log
    log_file = os.path.join(ERROR_LOG_DIR, f"{provider}.log")
    
    error_entry = {
        "timestamp": timestamp.isoformat(),
        "error_type": error_type,
        "query_context": query_context,
        "error_message": error_message,
    }
    
    if data:
        error_entry["data"] = data
    
    # Append to log file
    with open(log_file, 'a') as f:
        f.write(f"[{time_str}] {error_type} - {query_context}\n")
        f.write(f"Error: {error_message}\n")
        if data:
            f.write(f"Data: {json.dumps(data, indent=2)}\n")
        f.write("-" * 80 + "\n")