"""
It's the interface module of the package. Developers will start
interacting with the API/package using `Medium` Class object via 
different functions provided in it.
"""

import time
import re
from urllib.parse import urlparse, quote
from http.client import HTTPSConnection
from json import loads
from concurrent.futures import ThreadPoolExecutor, as_completed

from medium_api._topfeeds import TopFeeds
from medium_api._user import User
from medium_api._article import Article
from medium_api._publication import Publication
from medium_api._top_writers import TopWriters
from medium_api._latestposts import LatestPosts
from medium_api._medium_list import MediumList

class Medium:
    """Main Medium API Class to access everything

        Typical usage example:

        ``from medium_api import Medium``

        ``medium = Medium('YOUR_RAPIDAPI_KEY')``

    Args:
        rapidapi_key (str): A secret alphanumeric string value. To get your 
            RapidAPI key, please go to the following URL, register an account 
            and subscribe to Medium API (by Nishu Jain).

            https://rapidapi.com/nishujain199719-vgIfuFHZxVZ/api/medium2

        base_url (str, optional): It's the base URL of the API that is used by
            all the other endpoints. Currently, it is set to the RapidAPI's 
            domain (medium2.p.rapidapi.com). May change in the future according
            to where it's listed.

        calls (int, optional): It's an integer value for keeping track of all the
            API calls made by the Medium Class Object. Initially, it is set to 0.
            At the end of program, you can see the number of calls like this:

            ``print(medium.calls)``

    Returns:
        Medium: A `Medium` Class Object for the given *RAPIDAPI_KEY*. It can be
        used to access all the other functions such as: `user`, `article`, 
        `publication`, `topfeeds`, `top_writers`, etc ... 

    Note:
        See https://docs.rapidapi.com/docs/keys to learn more about RapidAPI keys.

    """
    def __init__(self, rapidapi_key:str, base_url:str='medium2.p.rapidapi.com', calls:int=0):
        if rapidapi_key and isinstance(rapidapi_key, str):
            self.headers = {
                'X-RapidAPI-Key': rapidapi_key,
                'User-Agent': f"medium-api-python-sdk"
            }
            self.base_url = base_url
            self.calls = calls
        else:
            print('[ERROR]: Please pass the API Key in string format')

    def __get_resp(self, endpoint:str, retries:int=0):
        conn = HTTPSConnection(self.base_url)
        conn.request('GET', endpoint, headers=self.headers)
        resp = conn.getresponse()

        data = resp.read()
        status = resp.status
        
        if status == 200:
            self.calls += 1
            json_data = loads(data)

            if not 'error' in json_data.keys():
                return json_data, status
            else:
                if retries < 3:
                    time.sleep(5)
                    return self.__get_resp(endpoint=endpoint, retries=retries+1)
                else:
                    print(f'[ERROR]: Response: {json_data}')
                    return {}, status
        else:
            print(f'[ERROR]: Status Code: {status}')
            print(f'[ERROR]: Response: {data}')
            return {}, status

    def user(self, username:str = None, user_id:str = None, save_info:bool = True):
        """For getting the Medium User Object

            Typical usage example:

            ``nishu = medium.user(username="nishu-jain")``

        Args:
            username (str, optional): It's your unique Medium username that
                you can find in the subdomain or at the end of the profile page
                URL as shown below.

                - ``username``.medium.com
                - medium.com/@ ``username``

                It's optional only if you've already provided the `user_id`.

            user_id (str, optional): It's your unique alphanumeric Medium ID that 
                cannot be changed. The User object is initialized using this only. 
                It's optional only if you've already provided the `username`.

            save_info (bool, optional): If `False`, creates an empty `User` object which
                needs to be filled using ``user.save_info()`` method later. (Default is 
                `True`)

        Returns:
            User: Medium API's User Object (medium_api._user.User) that can be used 
            to access all the properties and methods associated to the given Medium
            user.

        Note:
            You have to provide either `username` or `user_id` to get the User object. You
            cannot omit both. 
        """
        if user_id is not None:
            return User(user_id = user_id, 
                        get_resp = self.__get_resp, 
                        fetch_articles=self.fetch_articles,
                        fetch_users=self.fetch_users,
                        fetch_publications=self.fetch_publications,
                        fetch_lists=self.fetch_lists,
                        save_info = save_info)
        elif username is not None:
            resp, _ = self.__get_resp(f'/user/id_for/{str(username)}')
            user_id = resp['id']
            return User(user_id = user_id, 
                        get_resp = self.__get_resp, 
                        fetch_articles=self.fetch_articles,
                        fetch_users=self.fetch_users,
                        fetch_publications=self.fetch_publications,
                        fetch_lists=self.fetch_lists,
                        save_info = save_info)
        else:
            print('[ERROR]: Missing parameter: Please provide "user_id" or "username" to call the function')
            return None

    def article(self, article_id:str, save_info:bool = True):
        """For getting the Medium Article Object

            Typical usage example:

            ``article = medium.article(article_id = "562c5821b5f0")``

        Args:
            article_id (str): It's the unique hash at the end of every Medium Article.
                You can see it at the end of URL as shown below:

                - https://nishu-jain.medium.com/about-me-nishu-jain-562c5821b5f0

            save_info (bool, optional): If `False`, creates an empty `Article` object which
                needs to be filled using ``article.save_info()`` method later. (Default is 
                `True`)

        Returns:
            Article: Medium API `Article` Object (medium_api._article.Article) that can be
            used to access all the properties and methods related to a Medium Article.

        """
        return Article(article_id = article_id, 
                       get_resp = self.__get_resp, 
                       fetch_articles=self.fetch_articles,
                       fetch_users = self.fetch_users,
                       fetch_publications=self.fetch_publications,
                       fetch_lists=self.fetch_lists,
                       save_info = save_info)
    
    def list(self, list_id:str, save_info:bool = True):
        """For getting the Medium List Object

            Typical usage example:

            ``medium_list = medium.list(list_id = "38f9e0f9bea6")``

        Args:
            list_id (str): It's the unique hash at the end of every Medium List URL.
                You can see it at the end of URL as shown below:

                - https://nishu-jain.medium.com/list/medium-api-38f9e0f9bea6

            save_info (bool, optional): If `False`, creates an empty `Medium List` object which
                needs to be filled using ``medium_list.save_info()`` method later. (Default is 
                `True`)

        Returns:
            MediumList: Medium API `Medium List` Object (medium_api._medium_list.MediumList) that can be
            used to access all the properties and methods related to a Medium List.

        """
        return MediumList(list_id = list_id, 
                       get_resp = self.__get_resp, 
                       fetch_articles=self.fetch_articles,
                       fetch_users = self.fetch_users,
                       fetch_publications=self.fetch_publications,
                       fetch_lists=self.fetch_lists,
                       save_info = save_info)

    def publication(self, publication_slug:str = None, publication_id:str = None, save_info:bool = True):
        """For getting the Medium Publication Object

            Typical usage example:

            ``publication = medium.publication(publication_slug = "towards-artificial-intelligence")``
            ``publication = medium.publication(publication_id = "98111c9905da")``

        Args:
            publication_slug (str, optional): It's a lowercased hyphen-separated unique string 
                alloted to each Medium Publication. It's optional only if you've already provided 
                the `publication_id`.

            publication_id (str, optional): It's the unique hash id of a Medium Publication. 
                It's optional only if you've already provided the `publication_slug`.

            save_info (bool, optional): If `False`, creates an empty `Publication` object which
                needs to be filled using ``publication.save_info()`` method later. (Default is 
                `True`)

        Returns:
            Publication: Medium API `Publication` Object (medium_api._publication.Publication) 
            that can be used to access all the properties and methods related to a Medium 
            Publication.

        Note:
            You have to provide either `publication_slug` or `publication_id` to get the Publication object. 
            You cannot omit both. 

        """
        if publication_id is not None:
            return Publication(publication_id = publication_id, 
                        get_resp = self.__get_resp, 
                        fetch_articles=self.fetch_articles,
                        fetch_users=self.fetch_users,
                        fetch_publications=self.fetch_publications,
                        fetch_lists=self.fetch_lists,
                        save_info = save_info)

        elif publication_slug is not None:
            resp, _ = self.__get_resp(f'/publication/id_for/{str(publication_slug)}')
            publication_id = resp['publication_id']
            return Publication(publication_id = publication_id, 
                        get_resp = self.__get_resp, 
                        fetch_articles=self.fetch_articles,
                        fetch_users=self.fetch_users,
                        fetch_publications=self.fetch_publications,
                        fetch_lists=self.fetch_lists,
                        save_info = save_info)
        else:
            print('[ERROR]: Missing parameter: Please provide "publication_id" or "publication_slug" to call this function')
            return None

    def top_writers(self, topic_slug:str, count:int = 100):
        """For getting the Medium's TopWriters Object

            Typical usage example:

            ``top_writers = medium.top_writers(topic_slug = "artificial-intelligence")``

        Args:
            topic_slug (str): It's a string (smallcase, hyphen-separated) which specifies
                a category/niche as classified by the Medium Platform.

            count (int): Number of Top writers you want to fetch (less than 250).

        Returns:
            TopWriters: Medium API `TopWriters` Object (medium_api._top_writers.TopWriters) 
            that can be used to access all the properties and methods related to Medium's 
            Top Writers for the give `topic_slug`.

        """
        return TopWriters(topic_slug=topic_slug, 
                          count = count,
                          get_resp=self.__get_resp, 
                          fetch_users=self.fetch_users,
                          fetch_articles=self.fetch_articles,
                          fetch_publications=self.fetch_publications,
                          fetch_lists=self.fetch_lists,
                          )

    def latestposts(self, topic_slug:str):
        """For getting the Medium's LatestPosts Object

            Typical usage example:

            ``latestposts = medium.latestposts(topic_slug = "artificial-intelligence")``

        Args:
            topic_slug (str): It's a string (smallcase, hyphen-separated) which specifies
                a category/niche as classified by the Medium Platform.

        Returns:
            LatestPosts: Medium API `LatestPosts` Object (medium_api._latestposts.LatestPosts) 
            that can be used to access all the properties and methods related to Medium's 
            LatestPosts within the given topic.

        """
        return LatestPosts(topic_slug=topic_slug, 
                           get_resp=self.__get_resp, 
                           fetch_articles=self.fetch_articles,
                           fetch_users=self.fetch_users,
                           fetch_publications=self.fetch_publications,
                           fetch_lists=self.fetch_lists,
                        )

    def topfeeds(self, tag:str, mode:str, count:int = 25):
        """For getting the Medium's TopFeeds Object

            Typical usage example:

            ``topfeeds = medium.topfeeds(tag="blockchain", mode="new")``

        Args:
            tag (str): It's a string (smallcase, hyphen-separated) which specifies
                a category/niche as classified by the Medium Platform.
            
            count (int): Number of top feed articles you want to fetch (less than 250).

            mode (str): There are 6 modes as follows:

                    - ``hot``: For getting trending articles
                    - ``new``: For getting latest articles
                    - ``top_year``: For getting best articles of the year
                    - ``top_month``: For getting best articles of the month
                    - ``top_week``: For getting best articles of the week
                    - ``top_all_time``: For getting best article of all time


        Returns:
            TopFeeds: Medium API `TopFeeds` Object (medium_api._topfeeds.TopFeeds) 
            that can be used to access all the properties and methods, for given `tag` 
            and `mode`.

        """
        return TopFeeds(tag=tag, mode=mode, count=count,
                        get_resp=self.__get_resp, 
                        fetch_articles=self.fetch_articles,
                        fetch_users=self.fetch_users,
                        fetch_publications=self.fetch_publications,
                        fetch_lists=self.fetch_lists,
                    )
    
    def search_articles(self, query:str, save_info:bool=False):
        """To get the list of `Articles` for the given search query, from the Medium Platform.

            Typical usage example:

            ``ai_articles = medium.search_articles(query = "artificial intelligence")``

        Args:
            query (str): It's the search query to get results from Medium Platform.

            save_info (bool, optional): If `True`, the function will fetch article-related info for all the
                articles in the search result, using multi-threading. Else, the returned list will contain
                the empty `Article` objects. Default is `False`.

        Returns:
            list[Article]: List of `Article` objects from the search results.

        Note:
            The resultant list will contain 1000 `Article` objects at max.
        
        Warnings:
            OveruseWarning: Don't set ``save_info = True`` unless you have enough API calls in your subscribed plan. You might either exhaust your current plan or incur overage.
        """
        resp, _ = self.__get_resp(f'/search/articles?query={quote(query)}')

        article_ids = resp['articles']
        articles = []

        if article_ids:
            articles = [self.article(article_id=article_id, save_info=False) for article_id in article_ids]
            if save_info:
                self.fetch_articles(articles)

        return articles
    
    def search_publications(self, query:str, save_info:bool=False):
        """To get the list of `Publications` for the given search query, from the Medium Platform.

            Typical usage example:

            ``mental_health_pubs = medium.search_publications(query = "mental health")``

        Args:
            query (str): It's the search query to get results from Medium Platform.

            save_info (bool, optional): If `True`, the function will fetch publication-related info for all the
                publications in the search result, using multi-threading. Else, the returned list will contain
                the empty `Publication` objects. Default is `False`.

        Returns:
            list[Publication]: List of `Publication` objects from the search results.

        Note:
            The resultant list will contain 1000 `Publication` objects at max.
        
        Warnings:
            OveruseWarning: Don't set ``save_info = True`` unless you have enough API calls in your subscribed plan. You might either exhaust your current plan or incur overage.
        """
        resp, _ = self.__get_resp(f'/search/publications?query={quote(query)}')

        publication_ids = resp['publications']
        publications = []
        
        if publication_ids:
            publications = [self.publication(publication_id=publication_id, save_info=False) for publication_id in publication_ids]
            if save_info:
                self.fetch_publications(publications)

        return publications
    
    def search_users(self, query:str, save_info:bool=False):
        """To get the list of `Users` for the given search query, from the Medium Platform.

            Typical usage example:

            ``data_engineers = medium.search_users(query = "data engineer")``

        Args:
            query (str): It's the search query to get results from Medium Platform.

            save_info (bool, optional): If `True`, the function will fetch user-related info for all the
                users in the search result, using multi-threading. Else, the returned list will contain
                the empty `User` objects. Default is `False`.

        Returns:
            list[User]: List of `User` objects from the search results.

        Note:
            The resultant list will contain 1000 `User` objects at max.
        
        Warnings:
            OveruseWarning: Don't set ``save_info = True`` unless you have enough API calls in your subscribed plan. You might either exhaust your current plan or incur overage.
        """
        resp, _ = self.__get_resp(f'/search/users?query={quote(query)}')

        user_ids = resp['users']
        users = []
        
        if user_ids:
            users = [self.user(user_id=user_id, save_info=False) for user_id in user_ids]
            if save_info:
                self.fetch_users(users)

        return users
    
    def search_lists(self, query:str, save_info:bool=False):
        """To get an array of `MediumList` objects for the given search query, from the Medium Platform.

            Typical usage example:

            ``startup_lists = medium.search_lists(query = "startup")``

        Args:
            query (str): It's the search query to get results from Medium Platform.

            save_info (bool, optional): If `True`, the function will fetch List-related info for all the
                Medium Lists in the search result, using multi-threading. Else, the returned array will contain
                the empty `MediumList` objects. Default is `False`.

        Returns:
            list[MediumList]: Array of `MediumList` objects from the search results.

        Note:
            The resultant list will contain 1000 `MediumList` objects at max.
        
        Warnings:
            OveruseWarning: Don't set ``save_info = True`` unless you have enough API calls in your subscribed plan. You might either exhaust your current plan or incur overage.
        """
        resp, _ = self.__get_resp(f'/search/lists?query={quote(query)}')

        list_ids = resp['lists']
        lists = []
        
        if list_ids:
            lists = [self.list(list_id=list_id, save_info=False) for list_id in list_ids]
            if save_info:
                self.fetch_lists(lists)

        return lists
    
    def search_tags(self, query:str):
        """To get the list of tags for the given search query, from the Medium Platform.

            Typical usage example:

            ``blockchain_tags = medium.search_tags(query = "blockchain")``

        Args:
            query (str): It's the search query to get results from Medium Platform.

        Returns:
            list[str]: List of lowercased, hyphen-separated strings of tags

        Note:
            The resultant list will contain 1000 tags at max.
        """
        resp, _ = self.__get_resp(f'/search/tags?query={quote(query)}')

        tags = resp['tags']

        return tags if tags else []

    def related_tags(self, given_tag:str):
        """For getting the list of related tags

            Typical usage example:

            ``related_tags = medium.related_tag(given_tag="blockchain")``

        Args:
            given_tag (str): It's a string (lowercase, hyphen-separated) which specifies
                             a category/niche as classified by the Medium Platform.

        Returns:
            list[str]: List of Related Tags (strings).

        """
        resp, _ = self.__get_resp(f'/related_tags/{given_tag}')

        return resp['related_tags']
    
    def tag_info(self, tag:str):
        """To get the tag-related information

            Typical usage example:

            ``blockchain_tag = medium.tag_info(given_tag="blockchain")``

        Args:
            tag (str): It's a string (lowercase, hyphen-separated) which specifies
                       a category/niche as classified by the Medium Platform.

        Returns:
            dict: Contains tag-related information

        """
        resp, _ = self.__get_resp(f'/tag/{tag}')

        return resp

    def fetch_articles(self, articles:list, content:bool = False, markdown:bool = False, html:bool = False, html_fullpage:bool = True):
        """To quickly fetch articles (info and content) using multithreading

            Typical usage example:

            ``medium.fetch_articles(latestposts.articles)``
            ``medium.fetch_articles(user.articles)``
            ``medium.fetch_articles(list_of_articles_obj)``

        Args:

            articles (list[Article]): List of (empty) Article objects to fill information 
                (and content) into it.

            content(bool, optional): Set it to `True` if you want to fetch the content of 
                the article as well. Otherwise, default is `False`

            markdown(bool, optional): Set it to `True` if you want to fetch the markdown of 
                the article as well. Otherwise, default is `False`

            html(bool, optional): Set it to `True` if you want to fetch the article in HTML 
                format as well. Otherwise, default is `False`

            html_fullpage(bool, optional): Set it to `False` if you only want to fetch the HTML 
                inside body tag of the article. Otherwise, default is `True`, which fetches the 
                entire HTML of the article.

        Returns:
            None: This method doesn't return anything since it fills the values in the passed
            list of Article(s) objects itself.

        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = [executor.submit(article.save_info) for article in articles if article.title is None]
            if content:
                future_to_url += [executor.submit(article.save_content) for article in articles]

            if markdown:
                future_to_url += [executor.submit(article.save_markdown) for article in articles]

            if html:
                future_to_url += [executor.submit(article.save_html, html_fullpage) for article in articles]

            for future in as_completed(future_to_url):
                future.result()
    
    def fetch_publications(self, publications:list):
        """To quickly fetch publications' info using multithreading

            Typical usage example:

            ``medium.fetch_publications(user.publications)``
            ``medium.fetch_publications(list_of_publications_obj)``

        Args:

            publications (list[Publication]): List of (empty) Publications objects to fill information into it.

        Returns:
            None: This method doesn't return anything since it fills the values in the passed
            list of Publication(s) objects itself.

        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = [executor.submit(publication.save_info) for publication in publications if publication.name is None]

            for future in as_completed(future_to_url):
                future.result()

    def fetch_lists(self, medium_lists:list):
        """To quickly fetch Medium List related info using multithreading

            Typical usage example:

            ``medium.fetch_lists(user.lists)``
            ``medium.fetch_lists(arr_of_medium_list_objs)``

        Args:

            medium_lists (list[MediumList]): An array of (empty) `MediumList` objects to fill information into it.

        Returns:
            None: This method doesn't return anything since it fills the values in the passed
            array of MediumList(s) objects itself.

        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = [executor.submit(medium_list.save_info) 
                             for medium_list in medium_lists 
                             if medium_list.name is None]

            for future in as_completed(future_to_url):
                future.result()

    def fetch_users(self, users:list):
        """To quickly fetch users' info using multithreading

            Typical usage example:

            ``medium.fetch_users(top_writers.users)``
            ``medium.fetch_users(list_of_users_obj)``

        Args:

            users (list[User]): List of (empty) User objects to fill information into it.

        Returns:
            None: This method doesn't return anything since it fills the values into the 
            passed list of User(s) objects itself.

        """
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = (executor.submit(user.save_info) for user in users if user.fullname is None)

            for future in as_completed(future_to_url):
                future.result()

    def extract_article_id(self, article_url:str):
        """To get `article_id` from the Article's URL

            Usage example:

            ``article_id = medium.get_article_id("https://nishu-jain.medium.com/about-me-nishu-jain-562c5821b5f0")``

        Args:

            article_url (str): URL as string type

        Returns:
            str: Returns `article_id` as string for valid URL, else returns `None`.

        """
        regex = r'(https?://[^\s]+)'
        urls = re.findall(regex, article_url)

        if urls:
            urlpath = urlparse(urls[0]).path
            if urlpath:
                last_location = urlpath.split('/')[-1]
                article_id = last_location.split('-')[-1]

                if article_id.isalnum():
                    return article_id

        return None