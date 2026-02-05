import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
SYRACUSE_API_KEY = os.environ.get('SYRACUSE_API_KEY')
LINKUP_API_KEY = os.environ.get('LINKUP_API_KEY')
EXA_API_KEY = os.environ.get('EXA_API_KEY')
NEWSAPI_API_KEY = os.environ.get('NEWSAPI_API_KEY')
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')
MAX_DATE = datetime.now(tz=timezone.utc)
MIN_DATE = MAX_DATE - timedelta(days=90)
