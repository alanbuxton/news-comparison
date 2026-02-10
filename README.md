# AI News comparison

Comparing three providers:
* [perplexity.ai](Perplexity)
* [syracuse.1145.am](Syracuse) (my side project)
* [linkup.so](Linkup)

It was prompted by me being underwhelmed with the Perplexity API, certainly compared to the Web UI.

# Running it yourself 

Copy `.env.sample` to `.env` and update with your keys.

Then

`uv run main.py`

# Results

See [results](results) for the history of previous tests. Summary below in reverse date order, newest first.

## 2026-02-10 summary

Added Exa and Tavily to the mix.
Syracuse continues to be the preferred option (ChatGPT & Claude). [2026-02-10-analysis.md](results/2026-02-10-analysis.md)

## 2026-02-01 summary

AI Analysis recommends Syracuse.
ChatGPT, Grok, Claude, Gemini prefer Syracuse. Copilot prefers Linkup. [2026-02-01-analysis.md](results/2026-02-01-analysis.md)

## 2026-01-06 summary

At first glance, looks Perplexity has improved a lot over the past 6-9 months, but it turns out this is mostly to do with showing old articles as if they are new ones. It is generating a lot of false positives, so not great if you want to rely on it as your source of company or industry news.

Syracuse is holding its own well for industry news.

I did some AI analysis too.
Under my account, Claude and ChatGPT both said that Syracuse was best. I didn't trust the analysis so I asked someone else to try on a separate account. On his account, Gemini preferred Syracuse, ChatGPT preferred LinkUp, Microsoft Copilot and Grok preferred Perplexity. I have some hypotheses about why this is the case - see [results/2026-01-06-AI-analysis](results/2026-01-06-AI-analysis/README.md)

## 2025-08-30 summary

Not much change in industry-wide news

After recent changes, Syracuse is now much stronger contender for company-specific news. Next focus for attention will be industry news. [2025-08-30-analysis.md](results/2025-08-30-analysis.md)

## 2025-05-27 summary

None of the 3 are great at reliably getting news for an industry sector and region combo

Linkup is best overall for company news.

It's given me some ideas on where I could tinker to improve Syracuse. I'll test them all out again in a few months to see how things have moved on and if one of these starts to pull away from the others. [2025-05-27-analysis.md](results/2025-05-27-analysis.md)


