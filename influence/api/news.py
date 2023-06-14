endpoint = 'https://newsapi.org/v2/top-headlines?country={country}&apiKey={api_key}'

import requests
import warnings
warnings.filterwarnings('ignore')

for country in ['us']:
    url = endpoint.format(country=country)
    response = requests.get(url=url, verify=False).json()
    articles = response['articles'][:10]
    
    for i, art in enumerate(articles,1):
        print(f"{i}) {art['title']}")
    
