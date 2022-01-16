from http.client import HTTPSConnection
from ujson import loads
import concurrent.futures

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

    def get_user_id(self, username):
        resp, _ = self.__get_resp(f'/user/id_for/{str(username)}')
        user_id = resp['id']
        return str(user_id)

    def get_user(self, user_id=None, username=None):
        if user_id is not None:
            resp, _ = self.__get_resp(f'/user/{str(user_id)}')
        elif username is not None:
            user_id = self.get_user_id(username)
            resp, _ = self.__get_resp(f'/user/{str(user_id)}')
        else:
            print('Missing parameter: Please provide "user_id" or "username" to call the function')
            return None

        return dict(resp)

    def get_user_articles_ids(self, user_id=None, username=None):
        if user_id is not None:
            resp, _ = self.__get_resp(f'/user/{str(user_id)}/articles')
        elif username is not None:
            user_id = self.get_user_id(username)
            resp, _ = self.__get_resp(f'/user/{str(user_id)}/articles')
        else:
            print('Missing parameter: Please provide "user_id" or "username" to call the function')
            return None

        article_ids = resp['associated_articles']
        return list(article_ids)

    def get_user_following(self, user_id=None, username=None):
        if user_id is not None:
            resp, _ = self.__get_resp(f'/user/{str(user_id)}/following')
        elif username is not None:
            user_id = self.get_user_id(username)
            resp, _ = self.__get_resp(f'/user/{str(user_id)}/following')
        else:
            print('Missing parameter: Please provide "user_id" or "username" to call the function')
            return None
        
        return list(resp['following'])

    def get_article_info(self, article_id):
        resp, _ = self.__get_resp(f'/article/{str(article_id)}')
        return dict(resp)

    def get_article_content(self, article_id):
        resp, _ = self.__get_resp(f'/article/{str(article_id)}/content')
        return str(resp['content'])

    def get_publication_info(self, publication_id):
        resp, _ = self.__get_resp(f'/publication/{str(publication_id)}')
        return dict(resp)

    def get_top_writers_ids(self, topic_slug):
        resp, _ = self.__get_resp(f'/top_writers/{str(topic_slug)}')
        top_writer_ids = resp['top_writers']
        return list(top_writer_ids)

    def get_latestposts_ids(self, topic_slug):
        resp, _ = self.__get_resp(f'/latestposts/{str(topic_slug)}')
        latestposts_ids = resp['latestposts']
        return list(latestposts_ids)

    def get_user_articles_info(self, user_id=None, username=None):
        articles = []

        if user_id is not None:
            article_ids = self.get_user_articles_ids(user_id)
        elif username is not None:
            user_id = self.get_user_id(username)
            article_ids = self.get_user_articles_ids(user_id)
        else:
            print('Missing parameter: Please provide "user_id" or "username" to call the function')
            return None

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = (executor.submit(self.get_article_info, article_id) for article_id in article_ids)

            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    article = future.result()
                except Exception as exc:
                    article = str(type(exc))
                finally:
                    articles.append(article)

        return articles # list of dict