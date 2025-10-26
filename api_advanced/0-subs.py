#!/usr/bin/python3
"""
Get the number of subscribers for a given subreddit.
"""
import requests


def number_of_subscribers(subreddit):
    """Return total subscribers for a subreddit or 0 if invalid."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; ALU_API_Project/1.0)'}

    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            data = response.json()
            return data.get('data', {}).get('subscribers', 0)
        else:
            return 0
    except Exception:
        return 0
