"""
Recommended Lists module containing `RecommendedLists` class.
"""


class RecommendedLists:
    """RecommendedLists Class
    
    With `RecommendedLists` object, you can use the following properties and methods:

        - recommended_lists.ids
        - recommended_lists.objs
        - recommended_feed.fetch_lists()

    Note:
        `RecommendedLists` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.recommended_lists`.

    """
    def __init__(self, tag, get_resp, fetch_articles, fetch_users, fetch_publications, fetch_lists):
        self.tag = str(tag)
        self.__get_resp = get_resp

        self.__fetch_articles = fetch_articles
        self.__fetch_users = fetch_users
        self.__fetch_publications = fetch_publications
        self.__fetch_lists = fetch_lists

        self.__ids = []
        self.__lists = None

    @property
    def ids(self):
        """To get a list of recommended_lists `list_ids`
        
        Returns:
            list[str]: An array of `list_ids` (str) from the recommended_lists for the given
            `tag`.
        
        """
        if not self.__ids:
            resp, _ = self.__get_resp(f'/recommended_lists/{self.tag}')
            self.__ids += list(resp['recommended_lists'])

        return self.__ids

    @property
    def objs(self):
        """To get a list of recommended_lists `MediumList` objects
        
        Returns:
            list[MediumList]: An array of `MediumList` objects from the recommended_lists for the given
            `tag`.
        
        """
        from medium_api._medium_list import MediumList

        if self.__lists is None:
            self.__lists = [MediumList(list_id = list_id, 
                                       get_resp=self.__get_resp, 
                                       fetch_articles=self.__fetch_articles,
                                       fetch_users=self.__fetch_users,
                                       fetch_publications=self.__fetch_publications,
                                       fetch_lists=self.__fetch_lists,
                                       save_info=False)
                                for list_id in self.ids]

        return self.__lists

    def fetch_lists(self):
        """To fetch all the Recommended Lists' information (using multithreading)

        Returns:
            None: All the fetched information will be access via recommended_lists.objs

            ``recommended_lists.objs[0].name``
            ``recommended_lists.objs[1].claps``
            ``recommended_lists.objs[2].description``
        """
        self.__fetch_lists(self.objs)
        
    def __repr__(self):
        return f'<RecommendedLists: {self.tag}>'