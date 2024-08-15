'''
Users Module
'''
from datetime import datetime


SAMPLE_STYLE_FILE = 'https://mediumapi.com/styles/dark.css'

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
        - user.all_followers_ids
        - user.all_followers
        - user.interests
        - user.articles_as_json
        - user.publication_ids
        - user.publications
        - user.list_ids
        - user.lists

        - user.save_info()
        - user.fetch_articles()
        - user.fetch_top_articles()
        - user.fetch_following()
        - user.fetch_followers()
        - user.fetch_all_followers()
        - user.fetch_publications()
        - user.fetch_lists()

    Note:
        `User` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.user`.

    """
    def __init__(self, user_id, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists, save_info=False):
        self.user_id = user_id
        self.__get_resp = get_resp

        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__info = None
        self.__articles = None
        self.__article_ids = None
        self.__top_articles = None
        self.__top_article_ids = None
        self.__following_ids = None
        self.__following = None
        self.__followers_ids = None
        self.__publication_following_ids = None
        self.__publication_following = None
        self.__followers = None
        self.__all_followers_ids = None
        self.__all_followers = None
        self.__interests = None
        self.__list_ids = None
        self.__publication_ids = None
        self.__lists = None
        self.__publications = None

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
        self.top_writer_in = None
        self.has_list = None
        self.is_book_author = None
        self.tipping_link = None
        self.publication_following_count = None
        self.bg_image_url = None
        self.logo_image_url = None

        self.__books = None

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
            while resp['next']:
                resp, _ = self.__get_resp(f'/user/{self._id}/articles?next={resp["next"]}')
                self.__article_ids += list(resp['associated_articles'])

        return self.__article_ids
    
    @property
    def publication_ids(self):
        """To get a list of publication_ids where user is either creator and/or editor
        
        Returns:
            list[str]: A list of `publication_ids` (strings)
        
        """
        if self.__publication_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/publications')
            self.__publication_ids = resp['publications']

        return self.__publication_ids
    
    @property
    def list_ids(self):
        """To get an array of list_ids
        
        Returns:
            list[str]: An array of `list_ids` (str) by the user
        
        """
        if self.__list_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/lists')
            self.__list_ids = list(resp['lists'])

        return self.__list_ids
    
    @property
    def publications(self):
        """To get a list of `Publication` Objects where the user is either creator and/or editor
        
        Returns:
            list[Publication]: A list of `Publication` objects
        
        """
        from medium_api._publication import Publication

        if self.__publications is None:
            self.__publications = {
                                    "admin_in": [Publication(
                                        publication_id = pub_id,
                                        get_resp = self.__get_resp, 
                                        fetch_articles=self.__fetch_articles, 
                                        fetch_users = self.__fetch_users,
                                        fetch_publications=self.__fetch_publications,
                                        fetch_lists=self.__fetch_lists,
                                        save_info=False
                                        ) 
                                    for pub_id in self.publication_ids["admin_in"]],

                                    "writer_in": [Publication(
                                        publication_id = pub_id,
                                        get_resp = self.__get_resp, 
                                        fetch_articles=self.__fetch_articles, 
                                        fetch_users = self.__fetch_users,
                                        fetch_publications=self.__fetch_publications,
                                        fetch_lists=self.__fetch_lists,
                                        save_info=False
                                        ) 
                                    for pub_id in self.publication_ids["writer_in"]]
                            }
            
        return self.__publications
    
    @property
    def lists(self):
        """To get an array of `MediumList` Objects created by the user
        
        Returns:
            list[MediumList]: A list of `MediumList` objects
        
        """
        from medium_api._medium_list import MediumList

        if self.__lists is None:
            self.__lists = [MediumList(
                                        list_id = list_id,
                                        get_resp = self.__get_resp, 
                                        fetch_articles=self.__fetch_articles, 
                                        fetch_users = self.__fetch_users,
                                        fetch_publications=self.__fetch_publications,
                                        fetch_lists=self.__fetch_lists,
                                        save_info=False
                                      ) 
                            for list_id in self.list_ids]
            
        return self.__lists

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
    def interests(self):
        """To get a list of tags that the user follows.
        
        Returns:
            list[str]: A list of tags (str) followed by the user.
        
        """
        if self.__interests is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/interests')
            self.__interests = list(resp['tags_followed'])
        
        return self.__interests

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
    def publication_following_ids(self):
        """To get a list of `publications_ids` that the give user is followings
        
        Returns:
            list[str]: A list of `publication_ids` (str)
        
        """
        if self.__publication_following_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/publication_following')
            self.__publication_following_ids = list(resp['publication_following'])
        
        return self.__publication_following_ids
    
    @property
    def books(self):
        class UserBook(object): 
            def __init__(self, my_dict): 
                for key in my_dict: 
                    setattr(self, key, my_dict[key]) 

        if self.__books is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/books')
            self.__books = list([UserBook(book) for book in resp['books']])
        
        return self.__books
    
    @property
    def publication_following(self):
        """To get a list of `Publication` objects that the give user is followings
        
        Returns:
            list[Publication]: A list of `Publication` objects
        
        """
        from medium_api._publication import Publication

        if self.__publication_following is None:
            self.__publication_following = [Publication(
                                                publication_id = pub_id,
                                                get_resp = self.__get_resp, 
                                                fetch_articles=self.__fetch_articles, 
                                                fetch_users = self.__fetch_users,
                                                fetch_publications=self.__fetch_publications,
                                                fetch_lists=self.__fetch_lists,
                                                save_info=False
                                                ) 
                                            for pub_id in self.publication_following_ids]
        
        return self.__publication_following

    @property
    def followers_ids(self):
        """To get a list of `user_ids` of user's followers (length = 25)
        
        Returns:
            list[str]: A list of `user_ids` (str) of the user's followers (length = 25).
        
        """
        if self.__followers_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/followers')
            self.__followers_ids = list(resp['followers'])
        
        return self.__followers_ids
    
    @property
    def all_followers_ids(self):
        """To get a list of `user_ids` of user's followers (all). 
        This may take some time if the user has a lot of followers.
        
        Returns:
            list[str]: A list of `user_ids` (str) of the user's followers (all).
        
        """
        if self.__all_followers_ids is None:
            resp, _ = self.__get_resp(f'/user/{self._id}/followers')
            self.__all_followers_ids = list(resp['followers'])

            while resp['next']:
                resp, _ = self.__get_resp(f'/user/{self._id}/followers?count=25&after={resp["next"]}')
                self.__all_followers_ids += list(resp['followers'])
        
        return self.__all_followers_ids

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
                                    fetch_users = self.__fetch_users,
                                    fetch_publications=self.__fetch_publications,
                                    fetch_lists=self.__fetch_lists,
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
                                    fetch_users = self.__fetch_users,
                                    fetch_publications=self.__fetch_publications,
                                    fetch_lists=self.__fetch_lists,
                                    save_info = False
                              ) for user_id in self.followers_ids]
        
        return self.__followers
    
    @property
    def all_followers(self):
        """To get a full list of followers User objects
        
        Returns:
            list[User]: A list of `User` objects of followers
        
        """
        if self.__all_followers is None:
            self.__all_followers = [User(
                                    user_id = user_id,
                                    get_resp = self.__get_resp,
                                    fetch_articles = self.__fetch_articles,
                                    fetch_users = self.__fetch_users,
                                    fetch_publications=self.__fetch_publications,
                                    fetch_lists=self.__fetch_lists,
                                    save_info = False
                              ) for user_id in self.all_followers_ids]
        
        return self.__all_followers
        
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
                                    fetch_users = self.__fetch_users,
                                    fetch_publications=self.__fetch_publications,
                                    fetch_lists=self.__fetch_lists,
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
                                           fetch_users=self.__fetch_users,
                                           fetch_publications=self.__fetch_publications,
                                           fetch_lists=self.__fetch_lists,
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
                - ``user.has_list``
                - ``user.is_book_author``
                - ``user.allow_notes``
                - ``user.medium_member_at``
                - ``user.top_writer_in``
                - ``user.image_url``
                - ``user.tipping_link``
                - ``user.publication_following_count``
                - ``user.bg_image_url``
                - ``user.logo_image_url``
        """
        user = self.info

        self.fullname = user.get('fullname')
        self.username = user.get('username')
        self.followers_count = user.get('followers_count')
        self.following_count = user.get('following_count')
        self.bio = user.get('bio')
        self.twitter_username = user.get('twitter_username')
        self.is_writer_program_enrolled = user.get("is_writer_program_enrolled")
        self.image_url = user.get('image_url')
        self.is_suspended = user.get('is_suspended')
        self.allow_notes = user.get('allow_notes')
        self.has_list = user.get('has_list')
        self.is_book_author = user.get('is_book_author')
        self.tipping_link = user.get('tipping_link')
        self.publication_following_count = user.get('publication_following_count')
        self.bg_image_url = user.get('bg_image_url')
        self.logo_image_url = user.get('logo_image_url')

        if user.get('medium_member_at'):
            self.medium_member_at = datetime.strptime(user['medium_member_at'], '%Y-%m-%d %H:%M:%S') if user['medium_member_at']!='' else None
        self.top_writer_in = list(user['top_writer_in']) if user.get('top_writer_in') else []

        if self.fullname is None:
            print(f"[ERROR]: Could not retrieve user for the given user_id ({self.user_id}). Please check if this user exists.")
            print(f"[ERROR]: Link to unknown user's profile: https://medium.com/u/{self.user_id}")

    def fetch_articles(self, content=False, markdown=False, html=False, html_fullpage=True, html_style_file=SAMPLE_STYLE_FILE):
        """To fetch all the user-written articles information and content

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
            None: All the fetched information will be access via `user.articles`.

            ``user.articles[0].title``
            ``user.articles[1].claps``
        """
        self.__fetch_articles(
                    self.articles, 
                    content=content, 
                    markdown=markdown, 
                    html=html, 
                    html_fullpage=html_fullpage,
                    html_style_file=html_style_file
                )

    def fetch_publications(self, admin_in=True, writer_in=True):
        """To fetch all the publication-related information where the given user is 
        either an admin (creator/editor) or a contributing writer.

        Returns:
            None: All the fetched information will be access via `user.publications`.

            ``user.publications['admin_in'][0].name``
            ``user.publications['writer_in'][1].followers``
        """
        if admin_in:
            self.__fetch_publications(self.publications['admin_in'])
        
        if writer_in:
            self.__fetch_publications(self.publications['writer_in'])

    def fetch_top_articles(self, content=False, markdown=False, html=False, html_fullpage=True, html_style_file=SAMPLE_STYLE_FILE):
        """To fetch top 10 user-written top articles information and content

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
            None: All the fetched information will be access via `user.top_articles`.

            ``user.top_articles[0].title``
            ``user.top_articles[1].claps``
        """
        self.__fetch_articles(
                        self.top_articles, 
                        content=content,
                        markdown=markdown, 
                        html=html, 
                        html_fullpage=html_fullpage,
                        html_style_file=html_style_file
                    )

    def fetch_following(self):
        """To get user's followings information

        Returns:
            None: All the fetched information will be access via `user.following`

            ``user.following[0].fullname``
            ``user.following[1].bio``
        """
        self.__fetch_users(self.following)

    def fetch_publication_following(self):
        """To get information related to publications that the user is following

        Returns:
            None: All the fetched information will be access via `user.publication_following`

            ``user.publication_following[0].name``
            ``user.publication_following[1].followers``
        """
        self.__fetch_publications(self.publication_following)

    def fetch_followers(self):
        """To get user's followers information (first 25)

        Returns:
            None: All the fetched information will be access via `user.followers`

            ``user.followers[0].fullname``
            ``user.followers[1].bio``
        """
        self.__fetch_users(self.followers)

    def fetch_all_followers(self):
        """To get user's followers information (all)

        Returns:
            None: All the fetched information will be access via `user.all_followers`

            ``user.all_followers[0].fullname``
            ``user.all_followers[1].bio``
        """
        self.__fetch_users(self.all_followers)

    def fetch_lists(self):
        """To get user's lists' related information

        Returns:
            None: All the fetched information will be access via `user.lists`

            ``user.lists[0].name``
            ``user.lists[1].count``
        """
        self.__fetch_lists(self.lists)

    def __repr__(self):
        r = ''

        if self.user_id:
            r += self.user_id 
        if self.username:
            r += f"({self.username})"

        return f"<User: {r}>"

