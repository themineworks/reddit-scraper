#!/usr/bin/env python3
"""Free Reddit data with full comment trees. Python, Node.js and cURL clients for the Reddit Scraper on Apify, pay per result.

Command-line client for the themineworks/reddit-scraper actor on Apify: runs it, waits for it
to finish and saves every result as JSON and CSV. Flags map 1:1 to the actor's input.
Free Apify account and API token: https://console.apify.com/sign-up
Docs and pricing: https://themineworks.com/actors/reddit-scraper/
"""
import argparse, csv, json, os, sys
from apify_client import ApifyClient

ACTOR = "themineworks/reddit-scraper"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--token", default=os.environ.get("APIFY_TOKEN"), help="Apify API token (or set APIFY_TOKEN)")
    ap.add_argument("--out", default="results", help="Output basename, writes .json and .csv")
    ap.add_argument("--mode", help="What to scrape")
    ap.add_argument("--subreddits", help="Comma-separated. List of subreddit names to scrape (without r/ prefix)")
    ap.add_argument("--search-query", help="Search query string")
    ap.add_argument("--username", help="Reddit username (without u/ prefix)")
    ap.add_argument("--post-urls", help="Comma-separated. Full Reddit post URLs to scrape with comments")
    ap.add_argument("--sort-by", help="How to sort posts")
    ap.add_argument("--timeframe", help="Time window when using sort=top")
    ap.add_argument("--max-posts", type=int, help="Maximum number of posts to scrape")
    ap.add_argument("--include-comments", action=argparse.BooleanOptionalAction, help="Fetch and include the comment tree for each post")
    ap.add_argument("--max-comments-per-post", type=int, help="Maximum number of top-level comments to fetch per post")
    ap.add_argument("--max-depth", type=int, help="How deep to recurse into comment reply threads")
    ap.add_argument("--after", help="Reddit 'after' cursor for resuming or deep historical backfill")
    a = ap.parse_args()
    if not a.token:
        sys.exit("Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up")

    run_input = {}
    if a.mode is not None: run_input["mode"] = a.mode
    if a.subreddits: run_input["subreddits"] = [s.strip() for s in a.subreddits.split(",") if s.strip()]
    if a.search_query is not None: run_input["searchQuery"] = a.search_query
    if a.username is not None: run_input["username"] = a.username
    if a.post_urls: run_input["postUrls"] = [s.strip() for s in a.post_urls.split(",") if s.strip()]
    if a.sort_by is not None: run_input["sortBy"] = a.sort_by
    if a.timeframe is not None: run_input["timeframe"] = a.timeframe
    if a.max_posts is not None: run_input["maxPosts"] = a.max_posts
    if a.include_comments is not None: run_input["includeComments"] = a.include_comments
    if a.max_comments_per_post is not None: run_input["maxCommentsPerPost"] = a.max_comments_per_post
    if a.max_depth is not None: run_input["maxDepth"] = a.max_depth
    if a.after is not None: run_input["after"] = a.after

    client = ApifyClient(a.token)
    print(f"Running {ACTOR} ...")
    run = client.actor(ACTOR).call(run_input=run_input)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    with open(a.out + ".json", "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    keys = []
    for it in items:
        keys += [k for k in it if k not in keys]
    if items:
        with open(a.out + ".csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
            w.writeheader()
            for it in items:
                w.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v, (list, dict)) else v for k, v in it.items()})
    print(f"Done: {len(items)} results saved to {a.out}.json and {a.out}.csv")


if __name__ == "__main__":
    main()
