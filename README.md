# Reddit Scraper: Posts, Comments & Search, No API Key

Honest Reddit scraping. Free to run: you pay only Apify platform compute. Deep historical backfill via after cursor. Full nested comment trees. Search, subreddit, user, and post modes.

**Run it on Apify:** [apify.com/themineworks/reddit-scraper](https://apify.com/themineworks/reddit-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/reddit-scraper](https://themineworks.com/actors/reddit-scraper/)

**Price:** From $1.00 per 1,000 results on Apify's higher plans ($2.00 on the free plan), plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Free actor. No per-result fee, no monthly rental
* Full nested comment trees with replies
* Deep historical backfill via cursor
* 4 modes: subreddit, search, user, post
* Empty results are never charged

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/reddit-scraper").call(run_input={
    "mode": "subreddit",
    "subreddits": [
        "python"
    ],
    "searchQuery": "lab grown diamonds engagement ring",
    "username": "spez"
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/reddit-scraper').call({
    "mode": "subreddit",
    "subreddits": [
        "python"
    ],
    "searchQuery": "lab grown diamonds engagement ring",
    "username": "spez"
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~reddit-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"mode": "subreddit", "subreddits": ["python"], "searchQuery": "lab grown diamonds engagement ring", "username": "spez"}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 reddit_scraper.py --token YOUR_APIFY_TOKEN --mode "subreddit" --subreddits "python" --search-query "lab grown diamonds engagement ring" --username "spez"
node reddit_scraper.mjs --token YOUR_APIFY_TOKEN --mode "subreddit" --subreddits "python" --search-query "lab grown diamonds engagement ring" --username "spez"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `mode` (required) | string | `"subreddit"` | What to scrape |
| `subreddits` | array | `[]` | List of subreddit names to scrape (without r/ prefix) |
| `searchQuery` | string |  | Search query string |
| `username` | string |  | Reddit username (without u/ prefix) |
| `postUrls` | array | `[]` | Full Reddit post URLs to scrape with comments |
| `sortBy` | string | `"hot"` | How to sort posts |
| `timeframe` | string | `"all"` | Time window when using sort=top |
| `maxPosts` | integer | `25` | Maximum number of posts to scrape |
| `includeComments` | boolean | `false` | Fetch and include the comment tree for each post |
| `maxCommentsPerPost` | integer | `100` | Maximum number of top-level comments to fetch per post |
| `maxDepth` | integer | `3` | How deep to recurse into comment reply threads |
| `after` | string |  | Reddit 'after' cursor for resuming or deep historical backfill |
| `skipPinnedPosts` | boolean | `false` | Skip mod-pinned/stickied posts at the top of subreddit listings |
| `monitorMode` | boolean | `false` | Run on a schedule and deliver ONLY results not seen in a previous run |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `id` | string | Reddit post ID (base36) |
| `name` | string | Reddit fullname (t3_) |
| `subreddit` | string | Name of the subreddit |
| `subreddit_id` | string | Reddit internal subreddit ID |
| `title` | string | Title of the post |
| `author` | string | Username of the post author |
| `score` | integer | Net upvote score of the post |
| `upvote_ratio` | number | Ratio of upvotes to total votes (0 to 1) |
| `url` | string | URL the post links to (or the Reddit post URL for self posts) |
| `permalink` | string | Full Reddit permalink URL |
| `selftext` | string | Body text of self posts |
| `is_self` | boolean | Whether the post is a self (text) post |
| `domain` | string | Domain of the linked URL |
| `flair` | string | Post flair text |
| `num_comments` | integer | Number of comments on the post |
| `created_utc` | number | Unix timestamp (UTC) when the post was created |
| `awards_count` | integer | Total number of awards received |
| `scraped_at` | string | ISO 8601 timestamp of when the record was scraped |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/reddit-scraper
```

## FAQ

### Does this scraper require a Reddit API key?

No. The Reddit Scraper works without any API key, OAuth token, or Reddit account. It accesses public subreddit data directly.

### Can I get full comment trees with this Reddit scraper?

Yes. The scraper returns full nested comment trees including replies to replies. Each comment includes author, score, timestamp, and parent relationship.

### What does pay-per-result mean for the Reddit scraper?

You pay only for posts that are successfully delivered. If a run returns zero results due to a private subreddit or network issue, no results are charged, only the small start fee.

### How far back can I scrape Reddit posts?

The scraper supports deep historical backfill using Reddit's after cursor. You can retrieve posts from years ago by chaining pagination runs.

### What modes are available?

Four modes: subreddit (all posts from a subreddit), search (keyword search across Reddit), user (a specific user profile and posts), and post (a single post with full comment tree).

### Is there genuinely no per-result fee?

Correct. The actor itself is free and you pay only Apify platform compute for the time a run uses. There is no per-row charge and no monthly rental.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Threads Scraper](https://themineworks.com/actors/threads-scraper/): Meta Threads data that returns actual data
* [LinkedIn Post Scraper](https://themineworks.com/actors/linkedin-post-search/): Search LinkedIn posts by keyword without login
* [Threads Search Scraper](https://themineworks.com/actors/threads-search-scraper/): Threads posts by keyword, with a standing brand watch

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
