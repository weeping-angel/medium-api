import concurrent.futures

class TopFeeds:
    def __init__(self, tag, mode, get_resp):
        self.tag = str(tag)
        self.mode = str(mode)
        self.__get_resp = get_resp

        self.__ids = None
        self.__articles = None

    @property
    def ids(self):
        if self.__ids is None:
            resp, _ = self.__get_resp(f'/topfeeds/{self.tag}/{self.mode}')
            self.__ids = list(resp['topfeeds'])

        return self.__ids

    @property
    def articles(self):
        from medium_apis.article import Article

        if self.__articles is None:
            self.__articles = [Article(article_id=article_id, get_resp=self.__get_resp) for article_id in self.ids]

        return self.__articles 

    def fetch_articles_info(self):
        if self.__articles is None:
            self.__articles = self.articles

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = (executor.submit(article.save_info) for article in self.__articles)

            for future in concurrent.futures.as_completed(future_to_url):
                future.result()