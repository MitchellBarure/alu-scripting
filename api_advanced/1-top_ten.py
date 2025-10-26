#!/usr/bin/python3
"""
Print the titles of the first 10 hot posts for a subreddit.

If the subreddit is invalid or the request fails, print None.
"""
import requests


def top_ten(subreddit):
    """Print first 10 hot post titles or None if subreddit is invalid."""
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://api.reddit.com/r/{}/hot".format(subreddit)

    headers = {
        "User-Agent": "python:alu.api_project.top10:v1.0.1 (by MitchellBarure)"
    }
    
    # Request a limit of 10 posts
    params = {"limit": 10}

    try:
        resp = requests.get(
            url,
            headers=headers,
            params=params,
            allow_redirects=False,
            timeout=5
        )

        # Handle non-200 status codes (404, 403, 429, or 302 redirect)
        if resp.status_code != 200:
            print(None)
            return

        # Check for empty response data or API errors within the JSON structure
        payload = resp.json()
        posts = payload.get("data", {}).get("children", [])
        
        if not posts:
            print(None)
            return

        # Print the titles of the posts
        for post in posts:
            title = post.get("data", {}).get("title")
            if title:
                print(title)

    except requests.exceptions.RequestException:
        # Catch network errors, timeouts, etc.
        print(None)
    except Exception:
        # Catch JSON decoding errors or unexpected structure issues
        print(None)
