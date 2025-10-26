#!/usr/bin/python3
"""
Recursively collect titles of all hot posts for a subreddit.

Returns:
- list of titles on success
- None if subreddit is invalid or request fails
"""
import requests


def recurse(subreddit, hot_list=None, after=None):
    """
    Recursively fetches hot posts and returns a list of titles.

    Args:
        subreddit (str): Subreddit name.
        hot_list (list): Accumulator for titles (handled internally).
        after (str): Pagination token from Reddit API.

    Returns:
        list or None
    """
    if hot_list is None:
        hot_list = []

    # Strong, descriptive User-Agent helps avoid 429s
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {
        "User-Agent": "ALU-API-Project2 (by MitchellBarure)",
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
        return None

    if resp.status_code != 200:
        return None

    payload = resp.json()
    data = payload.get("data", {})
    children = data.get("children", [])

    for post in children:
        title = post.get("data", {}).get("title")
        if title is not None:
            hot_list.append(title)

    after_token = data.get("after")
    if after_token:
        return recurse(subreddit, hot_list, after_token)

    return hot_list
