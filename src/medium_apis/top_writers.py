

class TopWriters:
    def __init__(self, topic_slug, get_resp, fetch_users, fetch_articles):
        self.topic_slug = str(topic_slug)
        self.__get_resp = get_resp
        self.__fetch_users = fetch_users
        self.__fetch_articles = fetch_articles

        self.__ids = None
        self.__users = None

    @property
    def ids(self):
        if self.__ids is None:
            resp, _ = self.__get_resp(f'/top_writers/{self.topic_slug}')
            self.__ids = list(resp['top_writers'])

        return self.__ids

    @property
    def users(self):
        from medium_apis.user import User

        if self.__users is None:
            self.__users = [User(user_id=user_id, 
                                 get_resp=self.__get_resp,
                                 fetch_articles=self.__fetch_articles) for user_id in self.ids]
        
        return self.__users

    def fetch_users(self):
        self.__fetch_users(self.users)