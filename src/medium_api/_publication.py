"""
Publication Module
"""
from functools import lru_cache
from datetime import datetime
from medium_api._user import User
class Newsletter:
    """Newsletter Class
    
    With `Newsletter` object, you can use the following properties and methods:

        - newsletter.id
        - newsletter.info

        - newsletter.save_info()

    Note:
        `Newsletter` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.publication.newsletter`.

    """
    def __init__(self, publication_id, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists, save_info=False):
        self.publication_id = publication_id
        self.__get_resp = get_resp
        
        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__info = None

        if save_info:
            self.save_info()
    
    @property
    def info(self):
        """To get the newsletter related information
        
        Returns:
            dict: A dictionary object containing `id, name, slug, subscribers,
            description, image_url, etc ...`
        
        """
        if self.__info is None:
            resp, _ = self.__get_resp(f'/publication/{self.publication_id}/newsletter')
            self.__info = dict(resp)

        return self.__info

    def save_info(self):
        """Saves the information related to the publication

        Note:
            Only after running ``newsletter.save_info()`` you can use the following
            variables:

                - ``newsletter.name``
                - ``newsletter.description``
                - ``newsletter.id``
                - ``newsletter.subscribers``
                - ``newsletter.image_url``
                - ``newsletter.slug``
                - ``newsletter.creator``

        """
        newsletter = self.info

        self.id = newsletter['id']
        self.name = newsletter['name']
        self.subscribers = newsletter['subscribers']
        self.slug = newsletter['slug']
        self.description = newsletter['description']
        self.image_url = newsletter['image']
        
        self.creator = User(user_id=newsletter['creator_id'], 
                            get_resp=self.__get_resp, 
                            fetch_articles=self.__fetch_articles, 
                            fetch_users=self.__fetch_users,
                            fetch_publications=self.__fetch_publications,
                            fetch_lists=self.__fetch_lists,
                            save_info=False
                        )

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
    def __init__(self, publication_id, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists, save_info=False):
        self.publication_id = str(publication_id)
        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.name = None
        self.description = None
        self.tagline = None
        self.followers = None
        self.slug = None
        self.tags = None
        self.creator = None
        self.editors = None
        self.domain = None
        self.twitter_username = None
        self.instagram_username = None
        self.facebook_pagename = None

        self.newsletter = Newsletter(publication_id=publication_id, 
                                     get_resp = self.__get_resp,
                                     fetch_articles = self.__fetch_articles,
                                     fetch_users = self.__fetch_users,
                                     fetch_publications=self.__fetch_publications,
                                     fetch_lists=self.__fetch_lists,
                                     save_info=False)

        self.__info = None

        #self.__article_ids = None
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
                - ``publication.tagline``
                - ``publication.followers``
                - ``publication.slug``
                - ``publication.tags``
                - ``publication.domain``
                - ``publication.creator``
                - ``publication.editors``
                - ``publication.twitter_username``
                - ``publication.instagram_username``
                - ``publication.facebook_pagename``

        """
        publication = self.info

        self.name = publication.get('name')
        self.description = publication.get('description')
        self.tagline = publication.get('tagline')
        self.followers = publication.get('followers')
        self.slug = publication.get('slug')
        self.tags = publication.get('tags')
        self.domain = publication.get('domain')
        self.twitter_username = publication.get('twitter_username')
        self.instagram_username = publication.get('instagram_username')
        self.facebook_pagename = publication.get('facebook_pagename')

        self.creator = User(user_id=publication['creator'], 
                            get_resp=self.__get_resp, 
                            fetch_articles=self.__fetch_articles, 
                            fetch_users=self.__fetch_users, 
                            fetch_publications=self.__fetch_publications,
                            fetch_lists=self.__fetch_lists,
                            save_info=False
                        ) if publication.get('creator') else None

        self.editors = [User(user_id=editor_id, 
                            get_resp=self.__get_resp, 
                            fetch_articles=self.__fetch_articles, 
                            fetch_users=self.__fetch_users, 
                            fetch_publications=self.__fetch_publications,
                            fetch_lists=self.__fetch_lists,
                            save_info=False
                        ) for editor_id in publication.get('editors') if editor_id]

        if self.name is None:
            print(f"[ERROR]: Could not retrieve publication for the given id ({self.publication_id}). Please check if this publication exists.")
            print(f"[ERROR]: Link to unknown publication: https://medium.com/u/{self.publication_id}")
    
   
    def articles_from_ids(self, article_ids):
        """A generic function to get `Article` Objects from article_ids (list).

        Args:
            article_ids (list[str]): List of ``article_ids`` (string)

        Returns:
            list[Article]: Returns a list of Article Objects.

        """
        from medium_api._article import Article

        return [Article(
                        article_id=article_id, 
                        get_resp=self.__get_resp, 
                        fetch_articles=self.__fetch_articles,
                        fetch_users = self.__fetch_users,
                        fetch_publications=self.__fetch_publications,
                        fetch_lists=self.__fetch_lists,
                    )
                for article_id in article_ids]
    
    
    @lru_cache(maxsize=16)
    def get_articles_between(self, _from=None, _to=None, content=False, markdown=False, html=False, html_fullpage=True):
        """To get publication articles within a datetime range.

            Example usage:
                
            ``publication.get_articles_between(_from=datetime.now(), _to=datetime.now() - timedelta(days=15))``

        Args:
            _from (datetime.datetime): Starting date of the interval

            _to (datetime.datetime): Ending date of the interval

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
            list[Article]: Returns a list of Article Objects (publication articles).

        Note:
            - If the ``_to`` parameter is not provided, then the function will return recent 25 
              articles from the given date (in ``_from`` parameter)

            - If the ``_from`` parameter is not provided, then the function will take current
              datetime value (``datetime.now()``)

            - If both the parameters, ``_from`` and ``_to``, are not provided, then the function 
              will return top recent 25 articles from the current datetime.

        
        """
        if _from is None:
            _from = datetime.now()
        
        if _from and _to:
            if _to < _from:
                resp,_ = self.__get_resp(f'/publication/{self._id}/articles?from={_from.isoformat()}')
                articles = self.articles_from_ids(resp['publication_articles'][::-1])
                next_to = datetime.strptime(resp['to'], '%Y-%m-%d %H:%M:%S')

                while next_to > _to:
                    resp,_ = self.__get_resp(f'/publication/{self._id}/articles?from={next_to.isoformat()}')
                    articles += self.articles_from_ids(resp['publication_articles'][::-1])
                    next_to = datetime.strptime(resp['to'], '%Y-%m-%d %H:%M:%S')
            
                self.__fetch_articles(
                                articles, 
                                content=content,
                                markdown=markdown, 
                                html=html, 
                                html_fullpage=html_fullpage
                            )

                self.__articles = [article for article in articles if (_to <= article.published_at <= _from)]

            else:
                print('[ERROR]: "from" date should be greater than "to" date. Try swapping both.')
                return []
        else:
            resp,_ = self.__get_resp(f'/publication/{self._id}/articles?from={_from.isoformat()}')
            self.__articles = self.articles_from_ids(resp['publication_articles'])
            self.__fetch_articles(
                        self.__articles,
                        content=content,
                        markdown=markdown, 
                        html=html, 
                        html_fullpage=html_fullpage
                    )
        
        return self.__articles
    
    @property
    def articles(self):
        """Returns top recent 25 articles

            Typical Example Usage:

            ``publication.articles[0].title``
            ``publication.articles[1].author``

        Returns:
            list[Article]: Returns a list of Article Objects
        """
        if self.__articles is None:
            self.__articles = self.get_articles_between()
        
        return self.__articles