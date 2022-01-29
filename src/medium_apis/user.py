import concurrent.futures

class User:
    def __init__(self, user_id, get_resp):
        self.user_id = user_id
        self.__get_resp = get_resp

        self.__posts = None
        self.__info = None
        self.__top_articles = None

    @property
    def _id(self):
        return str(self.user_id)
    
    @property
    def info(self):
        if self.__info is None:
            resp, _ = self.__get_resp(f'/user/{str(self.user_id)}')
            self.__info = dict(resp)
        
        return self.__info
    
    @property
    def article_ids(self):
        resp, _ = self.__get_resp(f'/user/{self._id}/articles')
        article_ids = resp['associated_articles']
        return list(article_ids)

    @property
    def top_article_ids(self):
        resp, _ = self.__get_resp(f'/user/{self._id}/top_articles')
        top_article_ids = resp['top_articles']
        return list(top_article_ids)

    @property
    def following(self):
        resp, _ = self.__get_resp(f'/user/{self._id}/following')
        return list(resp['following'])

    @property
    def articles(self):
        from medium_apis.article import Article

        if self.__posts is None:
            self.__posts = [Article(i, get_resp = self.__get_resp) for i in self.article_ids]
            
        return self.__posts

    @property
    def top_articles(self):
        from medium_apis.article import Article

        if self.__top_articles is None:
            self.__top_articles = [Article(i, get_resp = self.__get_resp) for i in self.top_article_ids]
            
        return self.__top_articles

    @property
    def articles_as_json(self):
        self.fetch_articles_info()
        self.fetch_articles_content()
        return [post.json for post in self.__posts]

    def save_info(self):
        user = self.info

        self.fullname = user['fullname']
        self.username = user['username']
        self.followers = user['followers']
        self.bio = user['bio']
        self.twitter_username = user['twitter_username']
        self.is_writer_program_enrolled = user["is_writer_program_enrolled"]
        self.image_url = user['image_url']

    def fetch_articles_info(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = (executor.submit(article.save_info) for article in self.articles if article.title is None)

            for future in concurrent.futures.as_completed(future_to_url):
                future.result()

    def fetch_articles_content(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = (executor.submit(article.save_content) for article in self.articles if article.content is None)

            for future in concurrent.futures.as_completed(future_to_url):
                future.result()

