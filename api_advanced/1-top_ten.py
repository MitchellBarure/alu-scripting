#!/usr/bin/python3
"""
Query Reddit API for the first 10 hot post titles of a subreddit.
Prints each title on its own line.
If subreddit is invalid, prints None.
"""
import requests


def top_ten(subreddit):
    """Print the first 10 'hot' post titles for the given subreddit."""
    if not subreddit or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        # Descriptive UA helps avoid 429/403 on Reddit
        "User-Agent": "alu-scripting-top-ten/1.0 (by u/MitchellBarure)"
    }
    params = {"limit": 10}

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,  # required by the task
            timeout=10
        )
    except requests.RequestException:
        print(None)
        return

    # Invalid subreddits often 30x to search results or return non-200
    if resp.status_code != 200:
        print(None)
        return

    # Parse JSON safely
    try:
        data = resp.json()
    except ValueError:
        print(None)
        return

    posts = data.get("data", {}).get("children", [])
    if not posts:
        return

    for post in posts[:10]:
        title = post.get("data", {}).get("title")
        if title:
            print(title)
