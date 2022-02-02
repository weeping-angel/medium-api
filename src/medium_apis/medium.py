"""
It's the interface module of the package. Developers will start
interacting with the APIs/package using `Medium` Class object via 
different functions provided in it.
"""

from http.client import HTTPSConnection
from ujson import loads
from concurrent.futures import ThreadPoolExecutor, as_completed

from medium_apis._topfeeds import TopFeeds
from medium_apis._user import User
from medium_apis._article import Article
from medium_apis._publication import Publication
from medium_apis._top_writers import TopWriters
from medium_apis._latestposts import LatestPosts

class Medium:
    """Main Medium APIs Class to access everything

        Typical usage example:

        ``from medium_apis import Medium``

        ``medium = Medium('YOUR_RAPIDAPI_KEY')``

    Args:
        rapidapi_key (str): A secret alphanumeric string value. To get your 
            RapidAPI key, please go to the following URL, register an account 
            and subscribe to Medium APIs (by Nishu Jain).

            https://rapidapi.com/nishujain1997.19@gmail.com/api/medium2

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
    def __init__(self, rapidapi_key, base_url='medium2.p.rapidapi.com', calls=0):
        self.headers = {
            'x-rapidapi-key': rapidapi_key
        }
        self.base_url = base_url
        self.calls = calls

    def __get_resp(self, endpoint):
        conn = HTTPSConnection(self.base_url)
        conn.request('GET', endpoint, headers=self.headers)
        resp = conn.getresponse()
        self.calls += 1
        return loads(resp.read()), resp.status

    def user(self, username=None, user_id=None):
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

        Returns:
            User: Medium API's User Object (medium_apis.user.User) that can be used 
            to access all the properties and methods associated to the given Medium
            user.

        Note:
            You have to provide either `username` or `user_id` to get the User object. You
            cannot omit both. 
        """
        if user_id is not None:
            return User(user_id = user_id, 
                        get_resp = self.__get_resp, 
                        fetch_articles=self.fetch_articles)
        elif username is not None:
            resp, _ = self.__get_resp(f'/user/id_for/{str(username)}')
            user_id = resp['id']
            return User(user_id = user_id, 
                        get_resp = self.__get_resp, 
                        fetch_articles=self.fetch_articles)
        else:
            print('Missing parameter: Please provide "user_id" or "username" to call the function')
            return None

    def article(self, article_id):
        """For getting the Medium Article Object

            Typical usage example:

            ``article = medium.article(article_id = "562c5821b5f0")``

        Args:
            article_id (str): It's the unique hash at the end of every Medium Article.
                You can see it at the end of URL as shown below:

                - https://nishu-jain.medium.com/about-me-nishu-jain-562c5821b5f0

        Returns:
            Article: Medium APIs `Article` Object (medium_apis.article.Article) that can be
            used to access all the properties and methods related to a Medium Article.

        """
        return Article(article_id = article_id, 
                       get_resp = self.__get_resp, 
                       fetch_articles=self.fetch_articles)

    def publication(self, publication_id):
        """For getting the Medium Publication Object

            Typical usage example:

            ``publication = medium.publication(publication_id = "98111c9905da")``

        Args:
            publication_id (str): It's the unique hash id of a Medium Publication.

        Returns:
            Publication: Medium APIs `Publication` Object (medium_apis.publication.Publication) 
            that can be used to access all the properties and methods related to a Medium 
            Publication.

        """
        return Publication(publication_id = publication_id, 
                           get_resp=self.__get_resp)

    def top_writers(self, topic_slug):
        """For getting the Medium's TopWriters Object

            Typical usage example:

            ``top_writers = medium.top_writers(topic_slug = "artificial-intelligence")``

        Args:
            topic_slug (str): It's a string (smallcase, hyphen-separated) which specifies
                a category/niche as classified by the Medium Platform.

        Returns:
            TopWriters: Medium APIs `TopWriters` Object (medium_apis.top_writers.TopWriters) 
            that can be used to access all the properties and methods related to Medium's 
            Top Writers for the give `topic_slug`.

        """
        return TopWriters(topic_slug=topic_slug, 
                          get_resp=self.__get_resp, 
                          fetch_users=self.fetch_users,
                          fetch_articles=self.fetch_articles)

    def latestposts(self, topic_slug):
        """For getting the Medium's LatestPosts Object

            Typical usage example:

            ``latestposts = medium.latestposts(topic_slug = "artificial-intelligence")``

        Args:
            topic_slug (str): It's a string (smallcase, hyphen-separated) which specifies
                a category/niche as classified by the Medium Platform.

        Returns:
            LatestPosts: Medium APIs `LatestPosts` Object (medium_apis.latestposts.LatestPosts) 
            that can be used to access all the properties and methods related to Medium's 
            LatestPosts within the given topic.

        """
        return LatestPosts(topic_slug=topic_slug, 
                           get_resp=self.__get_resp, 
                           fetch_articles=self.fetch_articles)

    def topfeeds(self, tag, mode):
        """For getting the Medium's TopFeeds Object

            Typical usage example:

            ``topfeeds = medium.topfeeds(tag="blockchain", mode="new")``

        Args:
            tag (str): It's a string (smallcase, hyphen-separated) which specifies
                a category/niche as classified by the Medium Platform.

            mode (str): There are 6 modes as follows:

                    - ``hot``: For getting trending articles
                    - ``new``: For getting latest articles
                    - ``top_year``: For getting best articles of the year
                    - ``top_month``: For getting best articles of the month
                    - ``top_week``: For getting best articles of the week
                    - ``top_all_time``: For getting best article of all time


        Returns:
            TopFeeds: Medium APIs `TopFeeds` Object (medium_apis.topfeeds.TopFeeds) 
            that can be used to access all the properties and methods, for given `tag` 
            and `mode`.

        """
        return TopFeeds(tag=tag, mode=mode, 
                        get_resp=self.__get_resp, 
                        fetch_articles=self.fetch_articles)

    def fetch_articles(self, articles, content=False):
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

        Returns:
            None: This method doesn't return anything since it fills the values in the passed
            list of Article(s) objects itself.

        """
        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = [executor.submit(article.save_info) for article in articles if article.title is None]
            if content:
                future_to_url += [executor.submit(article.save_content) for article in articles]

            for future in as_completed(future_to_url):
                future.result()

    def fetch_users(self, users):
        """To quickly fetch users info using multithreading

            Typical usage example:

            ``medium.fetch_users(top_writers.users)``
            ``medium.fetch_users(list_of_users_obj)``

        Args:

            users (list[User]): List of (empty) User objects to fill information into it.

        Returns:
            None: This method doesn't return anything since it fills the values into the 
            passed list of User(s) objects itself.

        """
        with ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = (executor.submit(user.save_info) for user in users if user.fullname is None)

            for future in as_completed(future_to_url):
                future.result()