

class User:
    def __init__(self, user_id, get_resp, fetch_articles):
        self.user_id = user_id
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles

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
            self.__posts = [Article(i, get_resp = self.__get_resp, fetch_articles=self.__fetch_articles) for i in self.article_ids]
            
        return self.__posts

    @property
    def top_articles(self):
        from medium_apis.article import Article

        if self.__top_articles is None:
            self.__top_articles = [Article(i, get_resp = self.__get_resp, fetch_articles=self.__fetch_articles) for i in self.top_article_ids]
            
        return self.__top_articles

    @property
    def articles_as_json(self):
        return [post.json for post in self.articles]

    def save_info(self):
        user = self.info

        self.fullname = user['fullname']
        self.username = user['username']
        self.followers = user['followers']
        self.bio = user['bio']
        self.twitter_username = user['twitter_username']
        self.is_writer_program_enrolled = user["is_writer_program_enrolled"]
        self.image_url = user['image_url']

    def fetch_articles(self, content=False):
        self.__fetch_articles(self.articles, content=content)

