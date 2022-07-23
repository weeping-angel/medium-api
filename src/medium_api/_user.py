'''
Users Module
'''
from datetime import datetime

class User:
    """User Class
    
    With `User` object, you can use the following properties and methods:

        - user._id
        - user.info
        - user.article_ids
        - user.articles
        - user.top_article_ids
        - user.top_articles
        - user.following_ids
        - user.following
        - user.followers_ids
        - user.followers
        - user.articles_as_json

        - user.save_info()
        - user.fetch_articles()
        - user.fetch_top_articles()

    Note:
        `User` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.user`.

    """
    def __init__(self, user_id, get_resp, fetch_articles, save_info=False):
        self.user_id = user_id
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles

        self.__info = None
        self.__articles = None
        self.__article_ids = None
        self.__top_articles = None
        self.__top_article_ids = None
        self.__following_ids = None
        self.__following = None
        self.__followers_ids = None
        self.__followers = None

        self.fullname = None
        self.username = None
        self.followers_count = None
        self.following_count = None
        self.bio = None
        self.twitter_username = None
        self.is_writer_program_enrolled = None
        self.is_suspended = None
        self.medium_member_at = None
        self.allow_notes = None
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
        if self.__article_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/articles')
            self.__article_ids = list(resp['associated_articles'])

        return self.__article_ids

    @property
    def top_article_ids(self):
        """To get a list of top 10 article_ids
        
        Returns:
            list[str]: A list of `article_ids` (str) of the top 10 posts 
            on the user's profile. (Usually, in chronological order)
        
        """
        if self.__top_article_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/top_articles')
            self.__top_article_ids = list(resp['top_articles'])

        return self.__top_article_ids

    @property
    def following_ids(self):
        """To get a list of `user_ids` of user's followings
        
        Returns:
            list[str]: A list of `user_ids` (str) of the user's followings.
        
        """
        if self.__following_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/following')
            self.__following_ids = list(resp['following'])
        
        return self.__following_ids

    @property
    def followers_ids(self):
        """To get a list of `user_ids` of user's followers
        
        Returns:
            list[str]: A list of `user_ids` (str) of the user's followers.
        
        """
        if self.__followers_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/followers')
            self.__followers_ids = list(resp['followers'])
        
        return self.__followers_ids

    @property
    def following(self):
        """To get a full list of following User objects
        
        Returns:
            list[User]: A list of `User` objects followed by the given user
        
        """
        if self.__following is None:
            self.__following = [User(
                                user_id = user_id,
                                get_resp = self.__get_resp,
                                fetch_articles = self.__fetch_articles,
                                save_info = False
                              ) for user_id in self.following_ids]
        
        return self.__following

    @property
    def followers(self):
        """To get a full list of followers User objects
        
        Returns:
            list[User]: A list of `User` objects of followers
        
        """
        if self.__followers is None:
            self.__followers = [User(
                                user_id = user_id,
                                get_resp = self.__get_resp,
                                fetch_articles = self.__fetch_articles,
                                save_info = False
                              ) for user_id in self.followers_ids]
        
        return self.__followers
        
    @property
    def articles(self):
        """To get a full list of user-written Article objects
        
        Returns:
            list[Article]: A list of `Article` objects written by the user
        
        """
        from medium_api._article import Article

        if self.__articles is None:
            self.__articles = [Article(i, 
                                    get_resp = self.__get_resp, 
                                    fetch_articles=self.__fetch_articles, 
                                    save_info=False) 
                            for i in self.article_ids]
            
        return self.__articles

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
                - ``user.followers_count``
                - ``user.following_count``
                - ``user.bio``
                - ``user.twitter_username``
                - ``user.is_writer_program_enrolled``
                - ``user.is_suspended``
                - ``user.allow_notes``
                - ``user.medium_member_at``
                - ``user.image_url``
        """
        user = self.info

        self.fullname = user['fullname']
        self.username = user['username']
        self.followers_count = user['followers_count']
        self.following_count = user['following_count']
        self.bio = user['bio']
        self.twitter_username = user['twitter_username']
        self.is_writer_program_enrolled = user["is_writer_program_enrolled"]
        self.image_url = user['image_url']
        self.is_suspended = user['is_suspended']
        self.allow_notes = user['allow_notes']
        self.medium_member_at = datetime.strptime(user['medium_member_at'], '%Y-%m-%d %H:%M:%S') if user['medium_member_at']!='' else None

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

    def fetch_top_articles(self, content=False):
        """To fetch top 10 user-written top articles information and content

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via `user.articles`.

            ``user.top_articles[0].title``
            ``user.top_articles[1].claps``
        """
        self.__fetch_articles(self.top_articles, content=content)

