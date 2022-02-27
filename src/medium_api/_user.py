'''
Users Module
'''

class User:
    """User Class
    
    With `User` object, you can use the following properties and methods:

        - user._id
        - user.info
        - user.article_ids
        - user.articles
        - user.top_article_ids
        - user.top_articles
        - user.following
        - user.articles_as_json

        - user.save_info()
        - user.fetch_articles()

    Note:
        `User` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.user`.

    """
    def __init__(self, user_id, get_resp, fetch_articles, save_info=False):
        self.user_id = user_id
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles

        self.__posts = None
        self.__info = None
        self.__top_articles = None

        self.fullname = None
        self.username = None
        self.followers = None
        self.bio = None
        self.twitter_username = None
        self.is_writer_program_enrolled = None
        self.image_url = None

        if save_info:
            self.save_info()

    @property
    def _id(self):
        """To get the user_id

        Returns:
            str: `user_id` of the object.
        
        """
        return str(self.user_id)
    
    @property
    def info(self):
        """To get the user related information
        
        Returns:
            dict: A dictionary object containing `fullname, username, followers,
            bio, twitter_username, image_url, etc ...`
        
        """
        if self.__info is None:
            resp, _ = self.__get_resp(f'/user/{self._id}')
            self.__info = dict(resp)
        
        return self.__info
    
    @property
    def article_ids(self):
        """To get a full list of article_ids
        
        Returns:
            list[str]: A list of `article_ids` (str) written by the user
        
        """
        resp, _ = self.__get_resp(f'/user/{self._id}/articles')
        article_ids = resp['associated_articles']
        return list(article_ids)

    @property
    def top_article_ids(self):
        """To get a list of top 10 article_ids
        
        Returns:
            list[str]: A list of `article_ids` (str) of the top 10 posts 
            on the user's profile. (Usually, in chronological order)
        
        """
        resp, _ = self.__get_resp(f'/user/{self._id}/top_articles')
        top_article_ids = resp['top_articles']
        return list(top_article_ids)

    @property
    def following(self):
        """To get a list of `user_ids` of user's followings
        
        Returns:
            list[str]: A list of `user_ids` (str) of the user's followings.
        
        """
        resp, _ = self.__get_resp(f'/user/{self._id}/following')
        return list(resp['following'])

    @property
    def articles(self):
        """To get a full list of user-written Article objects
        
        Returns:
            list[Article]: A list of `Article` objects written by the user
        
        """
        from medium_api._article import Article

        if self.__posts is None:
            self.__posts = [Article(i, 
                                    get_resp = self.__get_resp, 
                                    fetch_articles=self.__fetch_articles, 
                                    save_info=False) 
                            for i in self.article_ids]
            
        return self.__posts

    @property
    def top_articles(self):
        """To get a list of top 10 articles
        
        Returns:
            list[Article]: A list of `Article` objects of the top 10 
            posts on the user's profile. (Usually, in chronological order)
        
        """
        from medium_api._article import Article

        if self.__top_articles is None:
            self.__top_articles = [Article(i, 
                                           get_resp = self.__get_resp, 
                                           fetch_articles=self.__fetch_articles, 
                                           save_info=False) 
                                    for i in self.top_article_ids]
            
        return self.__top_articles

    @property
    def articles_as_json(self):
        """To get a list of JSON objects containing user info
        
        Returns:
            list[dict]: A list of JSON objects containing information related to all 
            the posts on the user's profile.
        
        """
        return [post.json for post in self.articles]

    def save_info(self):
        """Saves the information related to the user
        
        Note:
            Only after running ``user.save_info()`` you can use the following
            variables:

                - ``user.fullname``
                - ``user.username``
                - ``user.followers``
                - ``user.bio``
                - ``user.twitter_username``
                - ``user.is_writer_program_enrolled``
                - ``user.image_url``
        """
        user = self.info

        self.fullname = user['fullname']
        self.username = user['username']
        self.followers = user['followers']
        self.bio = user['bio']
        self.twitter_username = user['twitter_username']
        self.is_writer_program_enrolled = user["is_writer_program_enrolled"]
        self.image_url = user['image_url']

    def fetch_articles(self, content=False):
        """To fetch all the user-written articles information and content

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via `user.articles`.

            ``user.articles[0].title``
            ``user.articles[1].claps``
        """
        self.__fetch_articles(self.articles, content=content)

