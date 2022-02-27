import os
from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

user = medium.user(username='nishu-jain')

user.fetch_articles(content=True)

print(f'{"Title": <100} Content Length')
for article in user.articles:
    print(f'{article.title : <100} {len(article.content)}')
