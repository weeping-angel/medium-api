from datetime import datetime

class Article:
    def __init__(self, article_id, get_resp):
        self.__get_resp = get_resp
        self.article_id = str(article_id)

        self.title = None
        self.subtitle = None
        self.claps = None
        self.author = None
        self.url = None
        self.published_at = None
        self.publication_id = None
        self.tags = None
        self.topics = None
        self.last_modified_at = None
        self.reading_time = None
        self.word_count = None
        self.voters = None
        self.image_url = None

        self.publication = None

        self.__info = None
        self.__content = None

    def save_info(self):
        from medium_apis.user import User
        from medium_apis.publication import Publication

        article = self.info

        self.title = article['title']
        self.subtitle = article['subtitle']
        self.claps = article['claps']
        self.author = User(user_id=article['author'], get_resp=self.__get_resp)
        self.url = article['url']
        self.published_at = datetime.strptime(article['published_at'], '%Y-%m-%d %H:%M:%S')
        self.publication_id = article['publication_id']
        self.tags = article['tags']
        self.topics = article['topics']
        self.last_modified_at = datetime.strptime(article['last_modified_at'], '%Y-%m-%d %H:%M:%S')
        self.reading_time = article['reading_time']
        self.word_count = article['word_count']
        self.voters = article['voters']
        self.image_url = article['image_url']

        if not self.is_self_published:
            self.publication = Publication(publication_id=self.publication_id, get_resp=self.__get_resp)


    def save_content(self):
        self.__content = self.content

    @property
    def _id(self):
        return self.article_id

    @property
    def info(self):
        if self.__info is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}')
            self.__info = dict(resp)
            if not 'title' in self.__info.keys():
                return self.info
        
        return self.__info

    @property
    def is_self_published(self):
        article = self.info
        if article['publication_id'] != '*Self-Published*':
            return False
        else:
            return True

    @property
    def content(self):
        if self.__content is None:
            resp, _ = self.__get_resp(f'/article/{self.article_id}/content')
            self.__content = str(resp['content'])

        return self.__content

    @property
    def json(self):
        ret = self.info
        ret['content'] = self.content

        return ret