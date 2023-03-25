from datetime import date, datetime
from typing import Any


class Notice(object):
    """通知实体类
    """

    def __init__(self, id=0, url='', title='', content_preview='', publish_date: date=None, content='', source=''):
        self.__id = id
        self.__url = url
        self.__title = title
        self.__content_preview = content_preview
        self.publish_date = publish_date
        self.__content = content
        self.__source = source

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value == None:
            self.__id = 0
        self.__id = value

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if value == None:
            self.__url = ''
        self.__url = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if value == None:
            self.__title = ''
        self.__title = value

    @property
    def content_preview(self):
        return self.__content_preview

    @content_preview.setter
    def content_preview(self, value):
        if value == None:
            value = ''
        self.__content_preview = value

    @property
    def publish_date(self):
        return self.__publish_date.strftime("%Y-%m-%d")

    @publish_date.setter
    def publish_date(self, value: date):
        if isinstance(value, str):
            dt = datetime.strptime(value, '%Y-%m-%d')
            value = dt.date()
        self.__publish_date = value

    @property
    def content(self):
        return self.__content

    @content.setter
    def content(self, value):
        if value == None:
            self.__content = ''
        self.__content = value

    @property
    def source(self):
        return self.__source

    @source.setter
    def source(self, value):
        if value == None:
            self.__source = ''
        self.__source = value

    def get_properties(self) -> list:
        return self.id, self.url, self.title, self.content_preview, self.publish_date, self.content, self.source
