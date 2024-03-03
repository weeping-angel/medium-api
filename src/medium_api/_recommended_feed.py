"""
Recommended Feed module containing `Recommended Feed` class.
"""
import math


SAMPLE_STYLE_FILE = 'https://mediumapi.com/styles/dark.css'

class RecommendedFeed:
    """RecommendedFeed Class
    
    With `RecommendedFeed` object, you can use the following properties and methods:

        - recommended_feed.ids
        - recommended_feed.articles
        - recommended_feed.fetch_articles()

    Note:
        `RecommendedFeed` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.recommended_feed`.

    """
    def __init__(self, tag, count, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists):
        self.tag = str(tag)
        self.count = int(count)
        self.__get_resp = get_resp

        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__ids = []
        self.__articles = None

    @property
    def ids(self):
        """To get a list of recommended_feed `article_ids`
        
        Returns:
            list[str]: A list of `article_ids` (str) from the recommended_feed for the given
            `tag`.
        
        """
        articles_per_page = 25
        no_of_pages = math.ceil(self.count / articles_per_page)
        if not self.__ids:
            for page in range(1, no_of_pages + 1):
                resp, _ = self.__get_resp(f'/recommended_feed/{self.tag}?page={page}')
                self.__ids += list(resp['recommended_feed'])

        return self.__ids[:self.count]

    @property
    def articles(self):
        """To get a list of recommended_feed `Article` objects
        
        Returns:
            list[Article]: A list of `Article` objects from the recommended_feed for the given
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
        """To fetch all the recommended_feed articles information (multithreading)

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
            None: All the fetched information will be access via recommended_feed.articles.

            ``recommended_feed.articles[0].title``
            ``recommended_feed.articles[1].claps``
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
        return f'<RecommendedFeed: {self.tag}>'