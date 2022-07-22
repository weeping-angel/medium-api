"""
latestposts module
"""


class LatestPosts:
    """LatestPosts Class
    
    With `LatestPosts` object, you can use the following properties and methods:

        - latestposts.ids
        - latestposts.articles
        - latestposts.fetch_articles()

    Note:
        `LatestPosts` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.latestposts`.

    """
    def __init__(self, topic_slug, get_resp, fetch_articles):
        self.topic_slug = str(topic_slug)
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles

        self.__ids = None
        self.__posts = None

    @property
    def ids(self):
        """To get the article_ids of the latestposts

        Returns:
            list[str]: Returns a list of article ids (str).
        """
        if self.__ids is None:
            resp, _ = self.__get_resp(f'/latestposts/{self.topic_slug}')
            try:
                self.__ids = list(resp['latestposts'])
            except KeyError:
                print("[ERROR]: An error occurred when calling the latestposts endpoint. Please ensure that you have passed a valid topic slug. If you are unsure if the topic slug you are using is valid, consider using the Topfeeds endpoint instead.")
                print('\nInput Topic Slug: ', self.topic_slug)
                self.__ids = []

        return self.__ids

    @property
    def articles(self):
        """To get a list of Article objects of the latestposts

        Returns:
            list[Article]: Returns a list of `Article` objects.
        """
        from medium_api._article import Article

        if self.__posts is None:
            self.__posts = [Article(article_id=article_id, 
                                    get_resp=self.__get_resp, 
                                    fetch_articles=self.__fetch_articles,
                                    save_info=False) 
                            for article_id in self.ids]

        return self.__posts 

    def fetch_articles(self, content=False):
        """To fetch all the latestposts articles information (multithreading)

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via latestposts.articles.

            ``latestposts.articles[0].title``
            ``latestposts.articles[1].claps``
        """
        self.__fetch_articles(self.articles, content=content)