 #!/usr/bin/python3
"""
Get the number from subscribers for the chosen subreddit
"""
import requests

def number_of_subscribers(subreddit):
   url = "https://www.reddit.com/r/{subreddit}/about.json".format(subreddit=subreddit)
   headers = {'User-Agent': 'Mitchells_API_Project'}

#Do not allow redirects
   response = requests.get(url, headers=headers, allow_redirects=False)

   if response.status_code == 200:
      data = response.json()
      subscribers = data['data']['subscribers']
      return subscribers

   else:
      return 0
