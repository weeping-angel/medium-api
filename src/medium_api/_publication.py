"""
Publication Module
"""

class Publication:
    """Publication Class
    
    With `Publication` object, you can use the following properties and methods:

        - publication._id
        - publication.info
        - publication.articles
        - publication.save_info()
        - publication.fetch_articles()

    Note:
        `Publication` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.publication`.

    """
    def __init__(self, publication_id, get_resp, fetch_articles, save_info=False):
        self.publication_id = str(publication_id)
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles

        self.name = None
        self.description = None
        self.url = None
        self.tagline = None
        self.followers = None
        self.slug = None
        self.tags = None
        self.twitter_username = None
        self.instagram_username = None
        self.facebook_pagename = None

        self.__info = None

        self.__article_ids = None
        self.__articles = None

        if save_info:
            self.save_info()

    @property
    def _id(self):
        """To get the publication_id

        Returns:
            str: `publication_id` of the object.
        
        """
        return self.publication_id

    @property
    def info(self):
        """To get the publication related information
        
        Returns:
            dict: A dictionary object containing `name, slug, followers,
            description, tagline, url, twitter_username, tags, etc ...`
        
        """
        if self.__info is None:
            resp, _ = self.__get_resp(f'/publication/{self._id}')
            self.__info = dict(resp)

        return self.__info

    def save_info(self):
        """Saves the information related to the publication
        
        Note:
            Only after running ``publication.save_info()`` you can use the following
            variables:

                - ``publication.name``
                - ``publication.description``
                - ``publication.url``
                - ``publication.tagline``
                - ``publication.followers``
                - ``publication.slug``
                - ``publication.tags``
                - ``publication.twitter_username``
                - ``publication.instagram_username``
                - ``publication.facebook_pagename``

        """
        publication = self.info

        self.name = publication['name']
        self.description = publication['description']
        self.url = publication['url']
        self.tagline = publication['tagline']
        self.followers = publication['followers']
        self.slug = publication['slug']
        self.tags = publication['tags']

        self.twitter_username = publication['twitter_username']
        self.instagram_username = publication['instagram_username']
        self.facebook_pagename = publication['facebook_pagename']
    
    @property
    def article_ids(self):
        """To get the article_ids (top 25) from the Publication

        Returns:
            list[str]: Returns a list of article ids (str).
        """
        if self.__article_ids is None:
            resp, _ = self.__get_resp(f'/publication/{self._id}/articles')
            self.__article_ids = list(resp['publication_articles'])

        return self.__article_ids
    
    @property
    def articles(self):
        """To get a list of Article objects (top 25) from the Publication

        Returns:
            list[Article]: Returns a list of `Article` objects.
        """
        from medium_api._article import Article

        if self.__articles is None:
            self.__articles = [Article(
                                    article_id=article_id, 
                                    get_resp=self.__get_resp, 
                                    fetch_articles=self.__fetch_articles,
                                )
                                for article_id in self.article_ids]

        return self.__articles

    def fetch_articles(self, content=False):
        """To fetch publication articles information (using multithreading)

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via publication.articles.

            ``publication.articles[0].title``
            ``publication.articles[1].claps``
        """
        self.__fetch_articles(self.articles, content=content)