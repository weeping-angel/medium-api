import os
from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

# e.g. https://nishu-jain.medium.com/medium-apis-documentation-3384e2d08667
article = medium.article(article_id='3384e2d08667', save_info=False)

print(article.content)
