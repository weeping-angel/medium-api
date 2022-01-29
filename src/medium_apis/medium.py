from http.client import HTTPSConnection
from ujson import loads

from medium_apis.topfeeds import TopFeeds
from medium_apis.user import User
from medium_apis.article import Article
from medium_apis.publication import Publication
from medium_apis.top_writers import TopWriters
from medium_apis.latestposts import LatestPosts

class Medium:
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
        if user_id is not None:
            return User(user_id = user_id, get_resp = self.__get_resp)
        elif username is not None:
            resp, _ = self.__get_resp(f'/user/id_for/{str(username)}')
            user_id = resp['id']
            return User(user_id = user_id, get_resp = self.__get_resp)
        else:
            print('Missing parameter: Please provide "user_id" or "username" to call the function')
            return None

    def article(self, article_id):
        return Article(article_id = article_id, get_resp = self.__get_resp)

    def publication(self, publication_id):
        return Publication(publication_id = publication_id, get_resp=self.__get_resp)

    def top_writers(self, topic_slug):
        return TopWriters(topic_slug=topic_slug, get_resp=self.__get_resp)

    def latestposts(self, topic_slug):
        return LatestPosts(topic_slug=topic_slug, get_resp=self.__get_resp)

    def topfeeds(self, tag, mode):
        return TopFeeds(tag=tag, mode=mode, get_resp=self.__get_resp)