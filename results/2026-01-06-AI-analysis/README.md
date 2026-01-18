# AI analysis

## Process

Here is the prompt I used:

> Given the attached results from comparing different news providers, which one is the best? Please be sure to check that the published dates are the correct ones and that the story is primarily about the company or region/industry mentioned.

The file attached is [2026-01-06-results.txt](../2026-01-06-results.txt)

### Step 1 - using my own account

I used my own (personal) ChatGPT and Claude accounts. ChatGPT doesn't mention the word Syracuse in its chat history. Claude mentions it once a few months ago when I was experimenting plugging it into the Syracuse MCP server.

Both ChatGPT and Claude claimed that Syracuse was the best of the three. LinkUp was in second place and Perplexity in third.
* [Claude](v1-claude.md)
* [ChatGPT](v1-chatgpt.md)

Some of the analysis was incorrect, e.g. Claude criticised 2025/2026 dates as being "dates in the future", which is nonsense.

I wondered if the positive commentary about Syracuse was somehow on some broader context that the AIs have about me (even though I've never used them to discuss Syracuse except in the one case where I was plugging in an MCP server)

So I went to step 2

### Step 2 - phone a friend

I asked my brother who lives a good distance away from me, works in a different industry and does not have any relevant shared content with me to see what happened if he asked the same question to AIs. The outputs he got are in this folder with prefix name "another-"

Some of their analysis was incorrect, e.g. none of them picked up that the LinkUp and Perplexity articles often had wrong dates.

Nevertheless, here are their rankings:

* [ChatGPT](v2-chatgpt.md): LinkUp, Perplexity, Syracuse
* [CoPilot](v2-copilot.md): Perplexity, Syracuse, LinkUp
* [Gemini](v2-gemini.md): Syracuse, Perplexity, LinkUp
* [Grok](v2-grok.md): Perplexity, Syracuse, LinkUp

### A curious piece of content

Check out this line from my Claude's analysis: "For procurement and supplier intelligence purposes, **Syracuse** provides the most reliable, timely, and actionable company-specific news."

I never mentioned procurement or supplier intellingence in my prompt. But my job is about procurement supplier intelligence. My Claude chat history is bound to have plenty of stuff in it relating to procurement. Or perhaps my Claude account (gmail) gives away that I work in the procurement space. Or perhaps it has access to my blog or LinkedIn where I _have_ written about different news providers.

### Take-aways

1. It's flattering that Syracuse does pretty well across all the AIs. It gets 3 first places, 2 seconds and only 1 third place.
2. There is some subtle context-building which means the AI is absolutely shaping its content based on some content specific to you.
3. AI analysis is rife with errors. Even in this relatively simple analysis the analysis of dates was pretty poor.

Actually, the more I think of it, these sorts of issues - lack of consistency, errors in analysis, perhaps subtly trying to tell the reader what they think the reader wants to see - make this current crop of AI tools feel pretty human-like after all....



