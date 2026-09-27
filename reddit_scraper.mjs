#!/usr/bin/env node
// Node.js client for the themineworks/reddit-scraper actor on Apify: runs it and saves results.json.
// Flags map 1:1 to the actor's input. Free API token: https://console.apify.com/sign-up
// Docs and pricing: https://themineworks.com/actors/reddit-scraper/
import { ApifyClient } from 'apify-client';
import { writeFileSync } from 'node:fs';

const ACTOR = 'themineworks/reddit-scraper';

function parseArgs(argv) {
    const out = {};
    for (let i = 0; i < argv.length; i++) {
        if (!argv[i].startsWith('--')) continue;
        const key = argv[i].slice(2);
        out[key] = argv[i + 1] && !argv[i + 1].startsWith('--') ? argv[++i] : true;
    }
    return out;
}

const args = parseArgs(process.argv.slice(2));
const token = args.token || process.env.APIFY_TOKEN;
if (!token) {
    console.error('Provide --token or set APIFY_TOKEN. Free token: https://console.apify.com/sign-up');
    process.exit(1);
}

const runInput = {};
if (args['mode'] !== undefined) runInput.mode = String(args['mode']);
if (args['subreddits'] !== undefined) runInput.subreddits = String(args['subreddits']).split(',').map((s) => s.trim());
if (args['search-query'] !== undefined) runInput.searchQuery = String(args['search-query']);
if (args['username'] !== undefined) runInput.username = String(args['username']);
if (args['post-urls'] !== undefined) runInput.postUrls = String(args['post-urls']).split(',').map((s) => s.trim());
if (args['sort-by'] !== undefined) runInput.sortBy = String(args['sort-by']);
if (args['timeframe'] !== undefined) runInput.timeframe = String(args['timeframe']);
if (args['max-posts'] !== undefined) runInput.maxPosts = parseInt(args['max-posts'], 10);
if (args['include-comments'] !== undefined) runInput.includeComments = args['include-comments'] === true || args['include-comments'] === 'true';
if (args['max-comments-per-post'] !== undefined) runInput.maxCommentsPerPost = parseInt(args['max-comments-per-post'], 10);
if (args['max-depth'] !== undefined) runInput.maxDepth = parseInt(args['max-depth'], 10);
if (args['after'] !== undefined) runInput.after = String(args['after']);

const client = new ApifyClient({ token });
console.log(`Running ${ACTOR} ...`);
const run = await client.actor(ACTOR).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
writeFileSync('results.json', JSON.stringify(items, null, 2));
console.log(`Saved ${items.length} results to results.json`);
