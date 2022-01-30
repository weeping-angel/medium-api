import concurrent.futures


class LatestPosts:
    def __init__(self, topic_slug, get_resp, fetch_articles):
        self.topic_slug = str(topic_slug)
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles

        self.__ids = None
        self.__posts = None

    @property
    def ids(self):
        if self.__ids is None:
            resp, _ = self.__get_resp(f'/latestposts/{self.topic_slug}')
            self.__ids = list(resp['latestposts'])

        return self.__ids

    @property
    def articles(self):
        from medium_apis.article import Article

        if self.__posts is None:
            self.__posts = [Article(article_id=article_id, 
                                    get_resp=self.__get_resp, 
                                    fetch_articles=self.__fetch_articles) 
                            for article_id in self.ids]

        return self.__posts 

    def fetch_articles(self, content=False):
        self.__fetch_articles(self.articles, content=content)