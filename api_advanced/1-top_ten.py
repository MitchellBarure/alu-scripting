 #!/usr/bin/python3
"""
Queries the Reddit API and prints the titles of the first 10 hot posts listed for a given subreddit Prints None if subreddit is invalid.
"""
import requests

def top_ten(subreddit):
    """Print first 10hot posts titles or None if subreddit is invalid."""
    if subreddit is None or not isinstance(subreddit, str):
        print(None)
        return

    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; ALU_API_Project/1.0)'}
    params = {'limit': 10}

    try:
        resp = requests.get(
            url, headers=headers, params=params,
            allow_redirects=False, timeout=10
        )

        # If invalid subreddit or blocked by rate/redirect, print None
        if resp.status_code != 200:
            print(None)
            return

        data = resp.json()
        posts = data.get('data', {}).get('children', [])

        if not posts:
            print(None)
            return

        for post in posts[:10]:
            title = post.get('data', {}).get('title')
            if title is not None:
                print(title)
    except Exception:
        # Any network/JSON erroR
        print(None)
