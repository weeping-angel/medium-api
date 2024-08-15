"""
Recommended Users module containing `RecommendedUsers` class.
"""

class RecommendedUsers:
    """RecommendedUsers Class
    
    With `RecommendedUsers` object, you can use the following properties and methods:

        - recommended_users.ids
        - recommended_users.users
        - recommended_users.fetch_users()

    Note:
        `RecommendedUsers` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.recommended_users`.

    """
    def __init__(self, tag, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists):
        self.tag = str(tag)
        self.__get_resp = get_resp

        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__ids = []
        self.__users = None

    @property
    def ids(self):
        """To get a list of recommended_users `user_ids`
        
        Returns:
            list[str]: A list of `user_ids` (str) from the recommended_users for the given
            `tag`.
        
        """

        if not self.__ids:
            resp, _ = self.__get_resp(f'/recommended_users/{self.tag}')
            self.__ids += list(resp['recommended_users'])

        return self.__ids

    @property
    def users(self):
        """To get a list of recommended_users `User` objects
        
        Returns:
            list[User]: A list of `User` objects from the recommended_users for the given
            `tag`.
        
        """
        from medium_api._user import User

        if self.__users is None:
            self.__users = [
                                User(
                                    user_id=user_id, 
                                    get_resp=self.__get_resp, 
                                    fetch_articles=self.__fetch_articles,
                                    fetch_users=self.__fetch_users,
                                    fetch_publications=self.__fetch_publications,
                                    fetch_lists=self.__fetch_lists,
                                    save_info=False
                                    ) 
                                for user_id in self.ids
                            ]

        return self.__users

    def fetch_users(self):
        """To fetch all the Recommended Users information (multithreading)

        Returns:
            None: All the fetched information will be access via recommended_users.users.

            ``recommended_users.users[0].fullname``
            ``recommended_users.users[1].bio``
            ``recommended_users.users[1].followers_count``
        """
        self.__fetch_users(self.users)
        
    def __repr__(self):
        return f'<RecommendedUsers: {self.tag}>'