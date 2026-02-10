import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
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
    date_str = timestamp.strftime("%Y-%m-%d")
    time_str = timestamp.strftime("%H:%M:%S")
    
    # Create filename: errors/2026-02-07-Tavily.log
    log_file = os.path.join(ERROR_LOG_DIR, f"{date_str}-{provider}.log")
    
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