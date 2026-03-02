# Provider Comparison Report: News Aggregation for Business Intelligence

## Executive Summary

Based on analysis of 1,585 search results across 12 industry/location combinations from 5 news providers (Exa, Linkup, Perplexity, Syracuse, Tavily), this report evaluates which provider best serves business users preparing for strategic meetings.

**Recommendation: Syracuse is the best choice, with Perplexity as a strong alternative.**

## Detailed Provider Analysis

### 1. Syracuse ✅ RECOMMENDED

**Strengths:**
- **Zero errors** (0% error rate) - highest reliability
- **Company-focused news**: 33.3% of articles are genuine company activity (M&A, partnerships, launches)
- **Relevant industry coverage**: Strong focus on actual business events vs. market reports
- **Good summaries**: 362 characters average - sufficient detail without overwhelming
- **Real articles verified**: 
  - "Dow to Cut 4,500 Employees in AI Overhaul" (Breitbart, Jan 30, 2026) ✅
  - "After months of stability, polyethylene prices move higher" (Plastics News, Feb 5, 2026) ✅
  - "Maersk layoffs: Shipping giant to cut 1,000 jobs" (Mint, Feb 5, 2026) ✅
  
**Sample Quality Check (PE Resins in US):**
- Article 1: Dow layoffs announcement - genuine corporate news ✅
- Article 2: PE resin pricing update - industry pricing trends ✅
- Article 3: Corporate cost-cutting initiatives - strategic business news ✅

**Coverage:** 117 valid results across most industry/location combinations

**Weaknesses:**
- Smaller volume than Tavily
- No coverage for some combinations (e.g., Film Distribution in Midwest)

**Best for:** Strategic moves, M&A activity, key personnel changes, expansion activities, financial performance

---

### 2. Perplexity ✅ STRONG ALTERNATIVE

**Strengths:**
- **Zero errors** (0% error rate) - perfect reliability
- **Balanced content**: 21.7% market analysis + 21.7% company news
- **Longest summaries**: 365 characters average - detailed context
- **Good date accuracy**: Dates match publication dates accurately
- **High-quality sources**: Diverse mix of industry publications

**Sample Quality Check (PE Resins in US):**
- Article 1: "Viewpoint: New PE capacity favorable to buyers in 2026" (Argus Media) - industry analysis ✅
- Article 2: "Polyethylene Market Volume to Worth 167.69 Million Tons by 2035" (GlobeNewswire) - market forecast ✅
- Article 3: "COMMODITIES 2026: Global polyethylene packaging fundamentals" (S&P Global) - sector analysis ✅

**Coverage:** 46 valid results - smaller but high quality

**Weaknesses:**
- Limited volume (only 46 total results)
- 19.6% "About Us" content - higher false positive rate
- Not comprehensive across all combinations

**Best for:** Industry sector trends, market positioning updates, regulatory issues

---

### 3. Linkup ⚠️ UNRELIABLE

**Strengths:**
- When it works, provides good market reports (56% market analysis content)
- Summaries are detailed (265 characters average)

**Critical Weaknesses:**
- **55% error rate** - more than half of results fail ❌
- Only 50 valid results out of 111 attempts
- Very limited coverage - missing from many industry/location combinations
- Unreliable for time-sensitive research

**Sample Quality Check (PE Resins in US):**
- Article 1: "Viewpoint: New PE capacity favorable to buyers in 2026" (Argus Media) - good ✅
- But 61 errors in dataset vs only 50 valid results ❌

**Verdict:** Cannot recommend due to high failure rate

---

### 4. Exa ⚠️ MODERATE QUALITY

**Strengths:**
- Largest provider coverage (478 valid results)
- Good source diversity (231 unique sources)
- Consistent coverage across all industry/location combinations

**Significant Weaknesses:**
- **8.8% error rate** - 46 failed results ❌
- **High false positive rate**: Many results are:
  - Product catalogs and "About Us" pages (14.5% detected)
  - Market research report promotions (30.3% are market reports)
  - ChemAnalyst promotional content (not actual news)
  
**Sample Quality Issues (PE Resins in US):**
- Article 1: "Track Dinitrochlorobenzene (DNCB) Price Report" - This is promotional content for ChemAnalyst platform ❌
- Article 2: "January resin price hikes expected" (Plastics News) - Valid news ✅
- Article 3: "Low demand continues to pressurise recyclate prices" (Plastics News) - Valid news ✅

**Example of Poor Quality:**
"Welcome to ChemAnalyst, a next-generation platform for chemical and petrochemical intelligence where innovation meets practical insight..." - This is a product pitch, not news ❌

**Verdict:** Too much noise - requires extensive filtering

---

### 5. Tavily ❌ NOT RECOMMENDED

**Strengths:**
- Highest volume (787 valid results)
- Zero technical errors
- Comprehensive coverage

**Critical Weaknesses:**
- **30.2% false positives** - highest rate of "About Us"/product content ❌
- **Missing metadata**: 
  - No source attribution ("nan" for published_by)
  - No dates ("nan" for published_date) ❌
- **Cannot verify freshness or relevance**
- **Longest summaries** (938 chars) but often filled with navigation elements and website boilerplate

**Sample Quality Issues (PE Resins in US):**
- Article 1: "Americas top stories: weekly summary" - No date, no source attribution ❌
- Article 2: "Shore Capital-backed FirmaPak acquires Easy Plastic Containers" - Possibly behind paywall ❌
- Article 3: Many summaries include website navigation text, not actual content ❌

**Example of Poor Quality:**
"Sign in or Register + Sign In / Register Database + GP search..." - This is website navigation, not article content ❌

**Verdict:** Unusable for business intelligence due to missing metadata and high noise

---

## Comparative Analysis Matrix

| Provider   | Error Rate | Valid Results | Avg Summary | Real News % | Date Accuracy | Paywall Free |
|-----------|-----------|---------------|-------------|-------------|---------------|--------------|
| Syracuse  | 0%        | 117          | 362 chars   | ~80%        | Excellent     | Yes          |
| Perplexity| 0%        | 46           | 365 chars   | ~75%        | Excellent     | Mostly       |
| Linkup    | 55% ❌     | 50           | 265 chars   | ~75%        | Good          | Mostly       |
| Exa       | 8.8%      | 478          | 242 chars   | ~60%        | Good          | Mixed        |
| Tavily    | 0%        | 787          | 938 chars   | ~50%        | Unknown ❌     | Unknown      |

---

## Recommendations by Use Case

### For Strategic Meetings (Main Use Case) → **Syracuse**
Best for understanding what companies are actually doing:
- M&A announcements
- Personnel changes
- Expansion activities
- Financial performance
- Partnership announcements

### For Market Intelligence → **Perplexity**
Best for understanding industry trends:
- Sector analysis
- Market forecasts
- Regulatory changes
- Technology trends

### For Comprehensive Research → **Syracuse + Perplexity**
Use both providers together:
- Syracuse for company-specific news
- Perplexity for market context
- Total of ~160 articles to review

### Avoid:
- **Tavily**: Missing critical metadata (dates, sources)
- **Linkup**: Too unreliable (55% failure rate)
- **Exa**: Too much promotional/catalog content

---

## Specific Findings by Industry/Location

### Best Coverage:
- **Road Freight in Europe**: Syracuse (20), Linkup (20), Perplexity (7)
- **PE Resins in US**: Syracuse (8), Perplexity (5), Linkup (4)
- **Packaging in India**: Syracuse (46 combined), Perplexity (9)

### Poor Coverage:
- **Film Distribution in Midwest**: Only Exa and Tavily have significant results
- **Film in China**: Limited across all providers except Exa and Tavily

---

## Implementation Guidance

### Recommended Workflow:

1. **Start with Syracuse** - Get 8-20 results per query
   - Focus on company-specific news
   - Check for M&A, partnerships, executive changes

2. **Supplement with Perplexity** - Add 3-7 results per query
   - Get market context
   - Understand broader trends

3. **Total Review Time**: ~30-50 articles per industry/location
   - Manageable for pre-meeting prep
   - Sufficient for comprehensive understanding

### Quality Checks Before Meeting:
✅ Verify dates match article publication dates (±1 day for timezones)
✅ Check article is actual news, not product page
✅ Confirm source is reputable trade publication
✅ Ensure article content matches headline
✅ Test that links are accessible without paywall

---

## Conclusion

**Syracuse** provides the best signal-to-noise ratio for business intelligence, with zero errors, strong focus on genuine company news, and sufficient coverage across most industry/location combinations. **Perplexity** serves as an excellent complement for market-level insights.

Avoid Tavily (missing metadata), Linkup (unreliable), and Exa (too much promotional content).