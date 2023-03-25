from lxml import etree
import re
from datetime import date
try:
    import ujson as json
except:
    import json

try:
    from .notice import Notice
except ImportError:
    from notice import Notice


class PageParser(object):
    """解析器类
    """
    REG = re.compile(r'info/\d+/(\d+).htm', re.S)

    def __init__(self, page: str) -> None:
        self._page_content = page
        self._notices = []
        self._parse()

    def _parse(self):
        """解析页面
        """
        root = etree.HTML(self._page_content)
        elements = root.xpath("//ul[@class='secList pageList']/li")
        for e in elements:
            notice = Notice()
            notice.title = e.xpath("div[@class='r']//a/text()")[0]
            url = str(e.xpath("div[@class='r']//a/@href")[0])
            notice.url = url
            notice.id = self._get_id(url)
            content_review = e.xpath(
                "div[@class='r']/div[@class='intro']/text()")[0]
            content_review = content_review.replace('\\n', '').strip()
            notice.content_preview = content_review
            year, month = e.xpath("div[@class='l']/text()")[0].split('-')
            day = e.xpath("div[@class='l']/span/text()")[0]
            notice.publish_date = date(
                year=int(year), month=int(month), day=int(day))
            self._notices.append(notice)

    def _get_id(self, url: str) -> int:
        res = self.REG.findall(url)[0]
        return int(res)
    
    def get_notices(self) -> list[Notice]:
        return self._notices

    # def _parse_date(self, date_str: str) -> date:
    #     pass

    # def test(self):
    #     root = etree.HTML(self._page_content)
    #     elements = root.xpath("//ul[@class='secList pageList']/li")
    #     e = elements[0]
    #     print(type(e.xpath("div[@class='r']//a/@href")[0]))


if __name__ == "__main__":
    with open('sample.html', encoding='utf-8') as fp:
        parser = PageParser(fp.read())
        parser.test()
