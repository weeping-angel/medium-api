import concurrent.futures


class TopWriters:
    def __init__(self, topic_slug, get_resp):
        self.topic_slug = str(topic_slug)
        self.__get_resp = get_resp

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
            self.__users = [User(user_id=user_id, get_resp=self.__get_resp) for user_id in self.ids]
        
        return self.__users

    def fetch_users_info(self):
        if self.__users is None:
            self.__users = self.users

        with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
            future_to_url = (executor.submit(user.save_info) for user in self.__users)

            for future in concurrent.futures.as_completed(future_to_url):
                future.result()