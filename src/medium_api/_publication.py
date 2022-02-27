"""
Publication Module
"""

class Publication:
    """Publication Class
    
    With `Publication` object, you can use the following properties and methods:

        - publication._id
        - publication.info
        - publication.save_info()

    Note:
        `Publication` class is NOT intended to be used directly by importing.
        See :obj:`medium_api.medium.Medium.publication`.

    """
    def __init__(self, publication_id, get_resp, save_info=False):
        self.publication_id = str(publication_id)
        self.__get_resp = get_resp

        self.name = None
        self.description = None
        self.url = None
        self.tagline = None
        self.followers = None
        self.slug = None
        self.tags = None
        self.twitter_username = None
        self.instagram_username = None
        self.facebook_pagename = None

        self.__info = None

        if save_info:
            self.save_info()

    @property
    def _id(self):
        """To get the publication_id

        Returns:
            str: `publication_id` of the object.
        
        """
        return self.publication_id

    @property
    def info(self):
        """To get the publication related information
        
        Returns:
            dict: A dictionary object containing `name, slug, followers,
            description, tagline, url, twitter_username, tags, etc ...`
        
        """
        if self.__info is None:
            resp, _ = self.__get_resp(f'/publication/{self._id}')
            self.__info = dict(resp)

        return self.__info

    def save_info(self):
        """Saves the information related to the publication
        
        Note:
            Only after running ``publication.save_info()`` you can use the following
            variables:

                - ``publication.name``
                - ``publication.description``
                - ``publication.url``
                - ``publication.tagline``
                - ``publication.followers``
                - ``publication.slug``
                - ``publication.tags``
                - ``publication.twitter_username``
                - ``publication.instagram_username``
                - ``publication.facebook_pagename``

        """
        publication = self.info

        self.name = publication['name']
        self.description = publication['description']
        self.url = publication['url']
        self.tagline = publication['tagline']
        self.followers = publication['followers']
        self.slug = publication['slug']
        self.tags = publication['tags']

        self.twitter_username = publication['twitter_username']
        self.instagram_username = publication['instagram_username']
        self.facebook_pagename = publication['facebook_pagename']