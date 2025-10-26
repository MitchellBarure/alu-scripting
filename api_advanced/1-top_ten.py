#!/usr/bin/python3
"""
Print the titles of the first 10 hot posts for a subreddit.

If the subreddit is invalid or the request fails, print None.
"""
import time
import requests


def top_ten(subreddit):
    """Print first 10 hot post titles or None if subreddit is invalid."""
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    hosts = [
        "https://api.reddit.com",
        "https://old.reddit.com",
        "https://www.reddit.com",
    ]

    headers = {
        "User-Agent": (
            "linux:alu.api_advanced.top10:v1.0 "
            "(by /u/example_student)"
        ),
        "Accept": "application/json",
        "Connection": "close",
    }
    params = {"limit": 10, "raw_json": 1}

    for base in hosts:
        url = "{}/r/{}/hot.json".format(base, subreddit)

        # two attempts per host to ride out 429/403 bursts
        for _ in range(2):
            try:
                resp = requests.get(
                    url,
                    headers=headers,
                    params=params,
                    allow_redirects=False,
                    timeout=10
                )
            except Exception:
                # try again / next host
                break

            # Retry once on common transient blocks
            if resp.status_code in (302, 403, 429):
                time.sleep(1)
                continue

            if resp.status_code != 200:
                # move to next host
                break

            # Ensure we actually got JSON (not an HTML page)
            ctype = resp.headers.get("content-type", "")
            if "json" not in ctype:
                break

            try:
                payload = resp.json()
            except ValueError:
                break

            posts = payload.get("data", {}).get("children", [])
            if not posts:
                print(None)
                return

            for post in posts[:10]:
                title = post.get("data", {}).get("title")
                if title is not None:
                    print(title)
            return

    # All hosts/attempts failed
    print(None)
