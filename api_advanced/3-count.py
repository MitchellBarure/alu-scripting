#!/usr/bin/python3
"""
Recursively count keyword occurrences in titles of all hot posts
for a subreddit. Matching is case-insensitive and space-delimited
(so 'java!' / 'java.' / 'java_' do not count as 'java').
"""
import requests


def count_words(subreddit, word_list, after=None, acc=None, weights=None):
    """
    Prints the sorted counts (desc by count, then asc by word).
    Returns nothing (prints only). If subreddit invalid or no matches,
    prints nothing per spec.
    """
    # Initialize accumulators once
    if acc is None:
        acc = {}
    if weights is None:
        weights = {}
        # Build multiplicity for duplicates in word_list
        for w in word_list:
            lw = str(w).lower()
            weights[lw] = weights.get(lw, 0) + 1
            # Ensure every tracked word appears in acc (even if zero now)
            if lw not in acc:
                acc[lw] = 0

    # Build request
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "ALU-API-Project3 (by Mitchell_Barure)",
        "Accept": "application/json"
    }
    params = {"limit": 100}
    if after is not None:
        params["after"] = after

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10
        )
    except Exception:
        # Invalid/unreachable -> print nothing
        return

    if resp.status_code != 200:
        # Invalid subreddit or blocked -> print nothing
        return

    payload = resp.json()
    data = payload.get("data", {})
    children = data.get("children", [])

    # Count occurrences: space-delimited tokens only
    for post in children:
        title = post.get("data", {}).get("title", "")
        # Tokenize only by spaces; do not strip punctuation
        tokens = [t.lower() for t in title.split()]
        for t in tokens:
            if t in weights:
                acc[t] += weights[t]

    # Recurse if there is another page
    nxt = data.get("after")
    if nxt:
        count_words(subreddit, word_list, nxt, acc, weights)
        return

    # Finished: filter zeros, sort, and print
    results = [(w, c) for (w, c) in acc.items() if c > 0]
    if not results:
        return

    # Sort: count desc, then word asc
    results.sort(key=lambda x: (-x[1], x[0]))

    for w, c in results:
        print("{}: {}".format(w, c))
