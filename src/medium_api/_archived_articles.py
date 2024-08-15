"""
Archived Articles module containing `ArchivedArticles` class.
"""
import math


SAMPLE_STYLE_FILE = 'https://mediumapi.com/styles/dark.css'

class ArchivedArticles:
    """ArchivedArticles Class
    
    With `ArchivedArticles` object, you can use the following properties and methods:

        - archived_articles.ids
        - archived_articles.articles
        - archived_articles.fetch_articles()

    Note:
        `ArchivedArticles` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.archived_articles`.

    """
    def __init__(self, tag, count, year, month, next, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists):
        self.tag = str(tag)
        self.count = int(count)
        self.year = str(year)
        self.month = str(month)
        self.next = str(next)

        self.__get_resp = get_resp
        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__ids = []
        self.__articles = None

    @property
    def ids(self):
        """To get a list of archived_articles `article_ids`
        
        Returns:
            list[str]: A list of `article_ids` (str) from the archived_articles for the given
            `tag`.
        
        """        
        if not self.__ids:
            resp, _ = self.__get_resp(f'/archived_articles/{self.tag}?year={self.year}&month={self.month}&next={self.next}')
            self.__ids += list(resp['archived_articles'])

            while resp['next'] and len(self.__ids) < self.count:
                resp, _ = self.__get_resp(f'/archived_articles/{self.tag}?year={self.year}&month={self.month}&next={resp["next"]}')
                self.__ids += list(resp['archived_articles'])

                if len(self.__ids) >= self.count:
                    break

        return self.__ids[:self.count]

    @property
    def articles(self):
        """To get a list of archived_articles `Article` objects
        
        Returns:
            list[Article]: A list of `Article` objects from the archived_articles for the given
            `tag`.
        
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

    def fetch_articles(self, content=False, markdown=False, html=False, html_fullpage=True, html_style_file=SAMPLE_STYLE_FILE):
        """To fetch all the archived_articles information (using multithreading)

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
            None: All the fetched information will be access via archived_articles.articles.

            ``archived_articles.articles[0].title``
            ``archived_articles.articles[1].claps``
        """
        self.__fetch_articles(
                    self.articles, 
                    content=content, 
                    markdown=markdown, 
                    html=html, 
                    html_fullpage=html_fullpage,
                    html_style_file=html_style_file
                )
        
    def __repr__(self):
        return f'<ArchivedArticles: {self.tag}>'