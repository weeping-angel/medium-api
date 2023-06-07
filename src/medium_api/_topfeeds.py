"""
topfeeds module containing `TopFeeds` class.
"""

class TopFeeds:
    """TopFeeds Class
    
    With `TopFeeds` object, you can use the following properties and methods:

        - topfeeds.ids
        - topfeeds.articles
        - topfeeds.fetch_articles()

    Note:
        `TopFeeds` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.topfeeds`.

    """
    def __init__(self, tag, mode, count, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists):
        self.tag = str(tag)
        self.mode = str(mode)
        self.count = count if (0 < count <= 250) else 100
        self.__get_resp = get_resp

        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__ids = []
        self.__articles = None

    @property
    def ids(self):
        """To get a list of topfeeds `article_ids`
        
        Returns:
            list[str]: A list of `article_ids` (str) from the topfeeds for the given
            `tag` and `mode`.
        
        """
        if self.__ids == []:
            count_per_call = 25
            calls = int(self.count/count_per_call) + (1 if self.count % count_per_call != 0 else 0)

            for i in range(0, calls):
                resp, _ = self.__get_resp(f'/topfeeds/{self.tag}/{self.mode}?after={i*count_per_call}&count={count_per_call}')
                self.__ids += list(resp['topfeeds'])

        return self.__ids[:self.count]

    @property
    def articles(self):
        """To get a list of topfeeds `Article` objects
        
        Returns:
            list[Article]: A list of `Article` objects from the topfeeds for the given
            `tag` and `mode`.
        
        """
        from medium_api._article import Article

        if self.__articles is None:
            self.__articles = [Article(article_id=article_id, 
                                       get_resp=self.__get_resp, 
                                       fetch_articles=self.__fetch_articles,
                                       fetch_users=self.__fetch_users,
                                       fetch_publications=self.__fetch_publications,
                                       fetch_lists=self.__fetch_lists,
                                       save_info=False) 
                                for article_id in self.ids]

        return self.__articles

    def fetch_articles(self, content=False, markdown=False, html=False, html_fullpage=True):
        """To fetch all the topfeeds articles information (multithreading)

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.
            
            markdown(bool, optional): Set it to `True` if you want to fetch the markdown of 
                the article as well. Otherwise, default is `False`

            html(bool, optional): Set it to `True` if you want to fetch the article in HTML 
                format as well. Otherwise, default is `False`

            html_fullpage(bool, optional): Set it to `False` if you only want to fetch the HTML 
                inside body tag of the article. Otherwise, default is `True`, which fetches the 
                entire HTML of the article.

        Returns:
            None: All the fetched information will be access via topfeeds.articles.

            ``topfeeds.articles[0].title``
            ``topfeeds.articles[1].claps``
        """
        self.__fetch_articles(
                    self.articles, 
                    content=content, 
                    markdown=markdown, 
                    html=html, 
                    html_fullpage=html_fullpage
                )