endpoint = 'https://newsapi.org/v2/top-headlines?country={country}&apiKey=a328892bafb6438a95bd2669ab8fae6c'

import requests
import warnings
warnings.filterwarnings('ignore')

for country in ['us']:
    url = endpoint.format(country=country)
    response = requests.get(url=url, verify=False).json()
    articles = response['articles'][:10]
    
    for i, art in enumerate(articles,1):
        print(f"{i}) {art['title']}")
    