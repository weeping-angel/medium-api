"""
top_writers module
"""

class TopWriters:
    """TopWriters Class
    
    With `TopWriters` object, you can use the following properties and methods:

        - top_writers.ids
        - top_writers.users
        - top_writers.fetch_users()

    Note:
        `TopWriters` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.top_writers`.

    """
    def __init__(self, topic_slug, get_resp, fetch_users, fetch_articles):
        self.topic_slug = str(topic_slug)
        self.__get_resp = get_resp
        self.__fetch_users = fetch_users
        self.__fetch_articles = fetch_articles

        self.__ids = None
        self.__users = None

    @property
    def ids(self):
        """To get a list of top writer's `user_ids`

        Returns:
            list[str]: A list of `user_ids` of the top writers for the given topic/niche.
        
        """
        if self.__ids is None:
            resp, _ = self.__get_resp(f'/top_writers/{self.topic_slug}')
            self.__ids = list(resp['top_writers'])

        return self.__ids

    @property
    def users(self):
        """To get a list of `User` objects

        Returns:
            list[User]: A list of `User` objects of the top writers for given topic/niche.
        """
        from medium_api._user import User

        if self.__users is None:
            self.__users = [User(user_id=user_id, 
                                 get_resp=self.__get_resp,
                                 fetch_articles=self.__fetch_articles,
                                 save_info=False) 
                            for user_id in self.ids]
        
        return self.__users

    def fetch_users(self):
        """To fetch top writers (user) related information

        Args:
            content (bool, optional): Set it to `True` if you want to fetch the 
                textual content of the article as well. Otherwise, default is `False`.

        Returns:
            None: All the fetched information will be access via top_writers.users.

            ``top_writers.users[0].fullname``
            ``top_writers.users[1].bio``
        """
        self.__fetch_users(self.users)