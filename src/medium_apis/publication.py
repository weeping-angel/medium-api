class Publication:
    def __init__(self, publication_id, get_resp):
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

    @property
    def _id(self):
        return self.publication_id

    @property
    def info(self):
        if self.__info is None:
            resp, _ = self.__get_resp(f'/publication/{self._id}')
            self.__info = dict(resp)

        return self.__info

    def set_info(self):
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