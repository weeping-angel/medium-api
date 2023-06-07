"""
medium_list (not python list) module containing `MediumList` class.
"""
from datetime import datetime
from medium_api._user import User

class MediumList:
    """MediumList Class
    
    With `MediumList` object, you can use the following properties and methods:

        - medium_list._id
        - medium_list.info
        - medium_list.article_ids
        - medium_list.articles
        - medium_list.response_ids
        - medium_list.responses
        - medium_list.fetch_responses()
        - medium_list.fetch_articles()

    Note:
        `MediumList` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.Mediumlist`.

    """
    def __init__(self, list_id, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists, save_info=False):
        self.list_id = list_id
        self.__get_resp = get_resp
        
        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__article_ids = []
        self.__articles = None
        self.__response_ids = []
        self.__responses = None
        self.__info = None

        self.name = None
        self.description = None
        self.count = None
        self.created_at = None
        self.claps = None
        self.responses_count = None
        self.voters = None
        self.thumbnail = None
        self.author = None
        self.last_item_inserted_at = None

        if save_info:
            self.save_info()

    @property
    def _id(self):
        """To get the list_id

        Returns:
            str: `list_id` of the object.
        
        """
        return str(self.list_id)
    
    @property
    def info(self):
        """To get the MediumList-related information
        
        Returns:
            dict: A dictionary object containing `name, description, author, claps,
            voters, responses_count, thumbnail, article count, etc ...`
        
        """
        if self.__info is None:
            resp, _ = self.__get_resp(f'/list/{self._id}')
            self.__info = dict(resp)
        
        return self.__info
    
    def save_info(self):
        """Saves the information related to the Medium List
        
        Note:
            Only after running ``medium_list.save_info()`` you can use the following
            variables:

                - ``medium_list.name``
                - ``medium_list.description``
                - ``medium_list.author``
                - ``medium_list.count``
                - ``medium_list.responses_count``
                - ``medium_list.claps``
                - ``medium_list.voters``
                - ``medium_list.created_at``
                - ``medium_list.last_item_inserted_at``
                - ``medium_list.thumbnail``
        """
        medium_list = self.info

        self.name = medium_list.get('name')
        self.description = medium_list.get('description')
        self.count = medium_list.get('count')
        self.responses_count = medium_list.get('responses_count')
        self.claps = medium_list.get('claps')
        self.voters = medium_list.get('voters')
        self.thumbnail = medium_list.get('thumbnail')

        self.author = User(
                            user_id = medium_list.get('author'), 
                            get_resp = self.__get_resp, 
                            fetch_articles=self.__fetch_articles, 
                            fetch_users=self.__fetch_users, 
                            fetch_publications=self.__fetch_publications,
                            fetch_lists=self.__fetch_lists,
                            save_info=False
                          ) if medium_list.get('author') else None
        
        if medium_list.get('created_at'):
            self.created_at = datetime.strptime(medium_list['created_at'], '%Y-%m-%d %H:%M:%S') if medium_list['created_at']!='' else None
        
        if medium_list.get('last_item_inserted_at'):
            self.last_item_inserted_at = datetime.strptime(medium_list['last_item_inserted_at'], '%Y-%m-%d %H:%M:%S') if medium_list['last_item_inserted_at']!='' else None
        
        if self.name is None:
            print(f"[ERROR]: Could not retrieve Medium List for the given list_id ({self.list_id}). Please check if this Medium List exists.")
    
    @property
    def article_ids(self):
        """To get an array of `article_ids` of the articles present in the Medium List
        
        Returns:
            list[str]: A list of `article_ids` (str) from the Medium List.
        
        """
        if self.__article_ids == []:
            resp, _ = self.__get_resp(f'/list/{self.list_id}/articles')
            self.__article_ids += list(resp['list_articles'])

        return self.__article_ids
    
    @property
    def response_ids(self):
        """To get an array of `response_ids` of the comments on the Medium List
        
        Returns:
            list[str]: A list of `response_ids` (str) from comments on the Medium List.
        
        """
        if self.__response_ids == []:
            resp, _ = self.__get_resp(f'/list/{self.list_id}/responses')
            self.__response_ids += list(resp['responses'])

        return self.__response_ids

    @property
    def articles(self):
        """To get an array of Medium List's `Article` objects
        
        Returns:
            list[Article]: A list of `Article` objects from the Medium List.
        
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
                                for article_id in self.article_ids]

        return self.__articles
    
    @property
    def responses(self):
        """To get an array of Responses/Comments on Medium List (`Article` objects)
        
        Returns:
            list[Article]: A list of `Article` objects for the comments/responses on the Medium List.
        
        """
        from medium_api._article import Article

        if self.__responses is None:
            self.__responses = [Article(article_id=response_id, 
                                       get_resp=self.__get_resp, 
                                       fetch_articles=self.__fetch_articles,
                                       fetch_users=self.__fetch_users,
                                       fetch_publications=self.__fetch_publications,
                                       fetch_lists=self.__fetch_lists,
                                       save_info=False) 
                                for response_id in self.response_ids]

        return self.__responses

    def fetch_articles(self, content=False, markdown=False, html=False, html_fullpage=True):
        """To fetch all the Medium List's articles information (using multithreading)

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
            None: All the fetched information will be access via medium_list.articles.

            ``medium_list.articles[0].title``
            ``medium_list.articles[1].claps``
        """
        self.__fetch_articles(
                    self.articles, 
                    content=content,
                    markdown=markdown, 
                    html=html, 
                    html_fullpage=html_fullpage
                )

    def fetch_responses(self, content=False):
        """To fetch all the Medium List's Responses information (using multithreading)

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via medium_list.articles.

            ``medium_list.responses[0].title``
            ``medium_list.responses[1].claps``
        """
        self.__fetch_articles(self.responses, content=content)