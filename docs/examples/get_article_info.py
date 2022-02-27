import os
from medium_api import Medium

medium = Medium(os.getenv('RAPIDAPI_KEY'))

# e.g. https://nishu-jain.medium.com/medium-apis-documentation-3384e2d08667
article = medium.article(article_id='3384e2d08667')
author = article.author

author.save_info()

print('Author: ', author.fullname)
print('Profile URL: ', f'https://medium.com/@{author.username}')
