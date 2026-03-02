# 2026-03-02 analysis

## AI Analysis

Prompt used (Companies):

```
The attached file contains search results from different news providers: Exa, Linkup, Perplexity, Syracuse and Tavily. It covers searches for news about specific companies. The search results are for news over 3 months to Mar 2nd, 2026 and cover the following company names: ExxonMobil, Borouge, Sigma Chemtrade, HPCL Mittal Energy, L M Goes Embalagens, Westrock, International Paper, Dine Cartonnages, Jiangin Yonghe Packaging Products, Fritz Foss, Husky Technologies, KRC Custom Manufacturing, Braroll Acessorios Industriais, Jindal Films, Klöckner Pentaplast, Klockner Pentaplast, Entertainment Partners, Universal McCann, Little Island Productions, Commerzbank AG, Linklaters, CBS News, Deloitte, Bloomberg.

I need you to compare the results and summarise the pros and cons of each of these providers. Ensure you check all the articles from each provider.

The context is: I am a business user who is preparing for a meeting in a few days about our relationship with a particular company. This could be a meeting with a sales prospect, a meeting with a supplier or a meeting with a current customer. Or it could be for internal strategic planning.

To help me in these I need to know some high-level context about notable events for this company. I don't want lots of noise on day to day activities, but I do want stories that will give me a fuller picture of what the company is up to. This could include product launches, strategic moves, M&A activity, financial performance, investment news, regulatory issues or market positioning updates, expansion activities or key personnel changes.

Examples of desirable content:
- Product launches 
- Strategic moves
- M&A activity
- Financial performance
- Investment news
- Regulatory issues
- Market positioning updates
- Expansion activities
- Key personnel changes

Examples of undesirable content:
- A company's about us page
- Content from the company's product catalog
- Content aimed at general public about how to use a company's products
- Wider industry analysis that touches on this company

I don't want to have to click into dozens of articles to get the full picture. I want some results that I can skim to get a good idea about what the underlying story is. But I do need to know that I can click through to the source article for more detail if I want to.

Which provider should I use for this?

When assessing each story check that:
- It is are real article (as opposed to about us or product listings)
- It is genuinely about the company (false positives are a big problem)
- The date given in the results file match the real published date of the article (within a day or so to allow for timezone differences)
- The summary gives sufficient information on the story
- The underlying source web page can be accessed without any additional paywall
- It includes an activity to do with the company, rather than just general industry background

When providing your analysis give your reasoning and refer to specific articles to support your assessment.
```

File to attach: [companies.csv](companies.csv)


Prompt used (Industries):

```
The attached file contains search results from news providers: Exa, Linkup, Perplexity, Syracuse and Tavily. It covers searches for news about different combinations of industry and location. The search results are for news over 3 months to March 2nd, 2026. The cover stories on PE Resins in US; Film Distribution in Midwest; Film Entertainment: Film Distribution in Midwest; Packaging Boxes in IN; Packaging: Packaging Boxes in IN; Packaging: Packaging Boxes in india; Road Freight in Europe; MRO in South America; Film (BOPP Film, BOPET, PE Film etc) in CN; Flexible Packaging: Film (BOPP Film, BOPET, PE Film etc) in CN; Distribution Services (Distribution, Mastering, Localization etc) in Northern America; Film Entertainment: Distribution Services (Distribution, Mastering, Localization etc) in Northern America.

I need you to compare the results and summarise the pros and cons of each of these providers. Ensure you check all the articles from each provider.

The context is: I am a business user who is preparing for a meeting in a few days about our exposure to an industry / location combination. This could be an internal strategy meeting, a sales review of our target industries, or a review of our supply chain in particular regions.

To help me in these I need to know some high-level context about notable events for this industry and location. I don't want lots of noise on day to day activities, but I do want stories that will give me a fuller picture of what is happening in this industry / location combination. This could be industry analyses or it could be stories about companies in that industry.


Examples of desirable content:
- Industry sector trends
- Product launches 
- Strategic moves
- M&A activity
- Financial performance
- Investment news
- Regulatory issues
- Market positioning updates
- Expansion activities
- Key personnel changes

Examples of not relevant content:
- A company's about us page
- Content from the company's product catalog
- Content aimed at general public about how to use a company's products
- Wider industry analysis that touches on this company

I don't want to have to click into dozens of articles to get the full picture. I want some results that I can skim to get a good idea about what the underlying story is. But I do need to know that I can click through to the source article for more detail if I want to.

Which provider should I use for this?

When assessing each story check that:
- It is are real article (as opposed to about us or product listings)
- It is genuinely about the industry and location (false positives are a big problem)
- The date given in the results file match the real published date of the article (within a day or so to allow for timezone differences)
- The summary gives sufficient information on the story
- The underlying source web page can be accessed without any additional paywall

When providing your analysis give your reasoning and refer to specific articles to support your assessment.
```

File to attach: [industries.csv](industries.csv)

## AI Results

### ChatGPT (local account, no memory, only used for provider comparisons)

#### Companies 

Preferred: Perplexity with LinkUp as second place
Others:
Exa - Good raw material, but requires manual filtering.
Syracuse – High precision but not comprehensive enough alone.
Tavily – Too noisy for executive business context unless heavily filtered.

| Criteria                | Exa                | Linkup      | Perplexity    | Syracuse    | Tavily                           |
| ----------------------- | ------------------ | ----------- | ------------- | ----------- | -------------------------------- |
| Real articles           | ✅ Mostly           | ✅           | ✅             | ✅           | ⚠️ Many finance aggregator pages |
| Genuinely about company | ⚠️ Mixed           | ✅ Good      | ✅ Very strong | ✅ Strong    | ❌ Often indirect                 |
| Summary quality         | ⚠️ Basic           | ⚠️ Moderate | ✅ Best        | ⚠️ Moderate | ⚠️ Inconsistent                  |
| Strategic relevance     | ⚠️ Needs filtering | ✅ Good      | ✅ Excellent   | ✅ Good      | ❌ Often stock-noise              |
| Noise level             | Medium             | Low         | Very Low      | Low         | Very High                        |
| Volume                  | High               | Moderate    | Low           | Moderate    | Very High                        |
| Best for exec prep      | ⚠️                 | ✅           | ⭐ Best        | ⚠️          | ❌                                |

Full response: [chatgpt-companies.md](AI-analysis/chatgpt-companies.md)


#### Industry / Locations

Preferred: Syracuse, with Exa in 2nd place
Others:
- Linkup (technical quality issues)
- Tavily (volume too noisy)
- Perplexity (too shallow and too many report landing pages)


| Provider   | Signal Quality | Noise     | Metadata Accuracy | Strategic Relevance | Executive Skimmability |
| ---------- | -------------- | --------- | ----------------- | ------------------- | ---------------------- |
| Exa        | High           | Moderate  | Good              | Strong              | Good                   |
| Linkup     | Low            | High      | Poor              | Weak                | Poor                   |
| Perplexity | Moderate       | Moderate  | Good              | Limited depth       | Moderate               |
| Syracuse   | Very High      | Low       | Strong            | Excellent           | Excellent              |
| Tavily     | Mixed          | Very High | Inconsistent      | Uneven              | Poor                   |

Full response: [chatgpt-industries.md](AI-analysis/chatgpt-industries.md)

### Claude (local account, only used for provider comparison)

#### Companies

Syracuse and LinkUp both good contenders
Others:
- Perplexity (too much hallucination)
- Tavily (no dates)
- Exa (too much irrelevant content)


| Criterion | Exa | Linkup | Perplexity | Syracuse | Tavily |
|---|---|---|---|---|---|
| Coverage of all 24 companies | ✅ | 🟡 | 🟡 | ❌ | ✅ |
| Low false positive rate | ❌ | 🟡 | 🟡 | ✅ | ❌ |
| Dates always present | 🟡 | 🟡 | ✅ | ✅ | ❌ |
| Skim-ready summaries | ❌ | 🟡 | ✅ | ✅ | 🟡 |
| No hallucination risk | 🟡 | 🟡 | ❌ | ✅ | 🟡 |
| No paywall issues | 🟡 | ✅ | ✅ | ✅ | 🟡 |
| Coverage of obscure companies | ❌ | ❌ | ⚠️ | ❌ | ❌ |


Full response: [claude-companies.md](AI-analysis/claude-companies.md)

#### Industry / Locations

Syracuse best where it has coverage
Exa has broad coverage

Others
- Linkup (too many errors)
- Tavily (too much noise)
- Perplexity (hallucination)

Full response: [claude-industries.md](AI-analysis/claude-industries.md)