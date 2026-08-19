"""Canonical query text shared by all providers.

Query wording used to drift per client — some providers were told to prefer
"credible business, trade, specialized or regional news sources" and others
were not, which quietly advantaged the ones that got the steer. The substance
is defined once here so every provider is asked the same question.

Two forms exist because the APIs are genuinely different, not because the ask
differs:

  keyword — Exa, Tavily, Perplexity Search. Retrieval engines that match terms;
            a long instruction paragraph pollutes the match (Tavily also
            truncates at 400 chars).
  prose   — Linkup, Perplexity Agent. LLM-driven endpoints that read
            instructions and synthesise an answer.

Both carry the same topics and the same credibility instruction. Clients append
their own output-format wording (JSON schema shape, date window) on top, since
that is an API constraint rather than part of the question being asked.

Syracuse takes structured parameters rather than free text and so uses none of
this.
"""

# The substance of the ask. Company queries and industry queries are different
# questions and keep different topic lists — normalising them onto one list made
# industry queries company-shaped ("financial performance", "supplier risk") and
# Linkup returned zero articles for topics that previously returned ten. What is
# normalised is that every provider gets the same list for a given query type.
COMPANY_TOPICS = [
    "product launches, strategic moves and M&A activity",
    "financial performance and investment news",
    "regulatory issues and market positioning",
    "supplier risk",
    "regional relevance and expansion activities",
]

INDUSTRY_TOPICS = [
    "market trends and macroeconomic developments",
    "regulatory or policy updates",
    "major deals, innovations or disruptions",
    "key players and suppliers in the space",
]

# Terse forms of the same lists, for keyword engines.
COMPANY_KEYWORDS = (
    "product launches, M&A, financial performance, regulation, "
    "supplier risk, expansion"
)

INDUSTRY_KEYWORDS = (
    "market trends, regulation, deals, innovation, key players, suppliers"
)

CREDIBILITY = (
    "Only include content from credible business, trade, specialist or "
    "regional news outlets."
)

RECENCY = "Prioritise more recent news articles."


def industry_str(industry: str, industry_context: str) -> str:
    """e.g. "BOPET (plastic film)" — the context disambiguates terms like
    "Film" (plastic film, not cinema) and "Board" (paperboard, not governance)."""
    industry = industry.strip()
    context = (industry_context or "").strip()
    return f"{industry} ({context})" if context else industry


def _bullets(topics: list) -> str:
    return "\n".join(f"- {t}" for t in topics)


# --- keyword form -----------------------------------------------------------

def company_keyword_query(company: str) -> str:
    return f"{company} news: {COMPANY_KEYWORDS}"


def industry_keyword_query(industry: str, industry_context: str, location: str) -> str:
    return (
        f"{industry_str(industry, industry_context)} industry in {location} "
        f"news: {INDUSTRY_KEYWORDS}"
    )


# --- prose form -------------------------------------------------------------

def company_prose_query(company: str) -> str:
    return (
        f"Find recent news mentioning {company}.\n"
        f"Focus on:\n{_bullets(COMPANY_TOPICS)}\n\n"
        f"{CREDIBILITY} {RECENCY}\n"
        "For each source cited, provide a separate summary of that source's content."
    )


def industry_prose_query(industry: str, industry_context: str, location: str) -> str:
    return (
        f"Fetch recent news related to the "
        f"{industry_str(industry, industry_context)} industry in {location}.\n"
        f"Focus on:\n{_bullets(INDUSTRY_TOPICS)}\n\n"
        f"{CREDIBILITY} {RECENCY}\n"
        "For each source cited, provide a separate summary of that source's content."
    )
