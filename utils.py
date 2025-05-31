import os
from datetime import date, timedelta

PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')
SYRACUSE_API_KEY = os.environ.get('SYRACUSE_API_KEY')
PERPLEXITY_ENDPOINT = os.environ.get('PERPLEXITY_ENDPOINT')
SYRACUSE_ENDPOINT = os.environ.get('SYRACUSE_ENDPOINT')
LINKUP_API_KEY = os.environ.get('LINKUP_API_KEY')
MIN_DATE = date.today() - timedelta(days=90)
