import requests
from datetime import date
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient
from dateutil.relativedelta import relativedelta

class OnPassiveBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)
        self.headers = {"Content-type": "application/x-www-form-urlencoded"}
        self.endpoint = "https://onpassive.com/blog/wp-admin/admin-ajax.php"
        self.date = date.today()

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("p", {"class": "single-post-head"})
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find("p", {"class": "single-post-head"})
            a = title_tag.find("a")
            return self.formatURL(a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find("div", {"class": "date"})
            return self.formatPublishedOn(publishedOn.text)
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None
        return self.formatAuthors(None) 

    def getTags(self, tag):
        if tag is None:
            return None

        return self.formatTags(None)

    def updateDate(self):
        self.date = self.date - relativedelta(months=1)

    def monthHasData(self):
        page = self.getNextPage()
        soup = BeautifulSoup(page.content, "html.parser")
        posts = soup.find_all("div", {"class": "single-post"})
        return len(posts) > 0

    def getNextPage(self, page_num=1):
        data = {
            "month": self.date.month,
            "year": self.date.year,
            "pageNumber": page_num,
            "ppp": 10,
            "action": "load_more_posts_ajax"
        }
        resp = requests.post(self.endpoint, data=data, headers=self.headers)
        return resp

    def getResources(self):
        while self.monthHasData():
            page_num = 1
            while True:
                page = self.getNextPage(page_num=page_num)
                soup = BeautifulSoup(page.content, 'html.parser')

                posts = soup.find_all("div", {"class": "single-post"})
                if len(posts) == 0:
                    break
                for post in posts:
                    title = self.getTitle(post)
                    url = self.getURL(post)
                    
                    if title is None or url is None:
                        continue
                    
                    authors = self.getAuthors(post)
                    publishedOn = self.getPublishedOn(post)
                    tags = self.getTags(post)

                    if not self.db.resourceExists(url): 
                        result = self.db.handleResource(self.source_id, title, url, authors, tags, publishedOn)
                        if not result:
                            print(f"Resource cannot be created : {title}")
                            print(url, tags, authors, publishedOn, sep="\n")
                    elif self.refetch:
                        if not self.db.handleResource(self.source_id, title, url, authors, tags, publishedOn):
                            print(f"Resource cannot be updated : {title}")
                        continue
                    else:
                        return

                page_num += 1

            self.updateDate()

if __name__ == "__main__":
    title = "OnPassive Blog"
    url = "https://onpassive.com/blog/"
    icon = "https://yt3.ggpht.com/ytc/AMLnZu-xLUV0pSiWGmphWNb6Ljf6Raq_PTfraotcHHYmrQ=s900-c-k-c0x00ffffff-no-rj"
    dateFormat = "%d %b %Y"

    onpassiveblog_client = OnPassiveBlogClient(title, url, icon, dateFormat)
    onpassiveblog_client.getResources()
