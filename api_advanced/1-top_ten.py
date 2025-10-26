#!/usr/bin/python3
"""
Print titles of the first 10 hot posts for a subreddit.

If the subreddit is invalid or the request fails, print None.
"""
import requests


def top_ten(subreddit):
    """Print first 10 hot post titles or None if subreddit is invalid."""
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        # Descriptive UA (Reddit recommends a unique UA)
        "User-Agent": "linux:alu.api_advanced.top10:v1.0.0 "
                      "(by /u/example_student)",
        "Accept": "application/json"
    }
    params = {"limit": 10}

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,   # <- do NOT follow redirects
            timeout=10
        )
    except Exception:
        print(None)
        return

    # Only proceed on a clean 200 OK; otherwise print None
    if resp.status_code != 200:
        print(None)
        return

    # Now it's safe to parse JSON
    payload = resp.json()
    posts = payload.get("data", {}).get("children", [])
    if not posts:
        print(None)
        return

    for post in posts[:10]:
        title = post.get("data", {}).get("title")
        if title is not None:
            print(title)
