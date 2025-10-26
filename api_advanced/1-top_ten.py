#!/usr/bin/python3
"""
Print titles of the first 10 hot posts for a subreddit.

If the subreddit is invalid or the request fails, print None.
"""
import requests


def top_ten(subreddit):
    """Print first 10 hot post titles or None if subreddit is invalid."""
    # Basic type guard
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    # Use a descriptive, non-generic User-Agent to avoid 429s
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "ALU-API-Advanced/1.0 (by u_example_student)",
        "Accept": "application/json"
    }
    params = {"limit": 10}

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=10
        )

        # Reject anything that isn't a straight 200 OK
        if resp.status_code != 200:
            print(None)
            return

        payload = resp.json()
        posts = payload.get("data", {}).get("children", [])
        if not posts:
            print(None)
            return

        # Print up to 10 titles
        for post in posts[:10]:
            data = post.get("data", {})
            title = data.get("title")
            if title is not None:
                print(title)

    except Exception:
        # Any network/JSON error -> required fallback
        print(None)
