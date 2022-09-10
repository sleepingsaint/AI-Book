import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class HunchNetBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("h3", {"class": "entry-title"})
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find("h3", {"class": "entry-title"})
            a = title_tag.find("a")
            return self.formatURL(a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find("time", {"class": "entry-date"})
            print(publishedOn.text)
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

    def nextPageUrl(self, soup):
        try:
            pagination = soup.find("nav", {"class": "pagination"})
            next_page_url = pagination.find("a", {"class": "next"})
            if next_page_url is not None:
                return next_page_url['href']
            return None
        except:
            return None

    def getResources(self, page_url):
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        posts = soup.find_all("article", {"class": "post"})

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

        nextPageURL = self.nextPageUrl(soup)
        if nextPageURL is not None:
            self.getResources(nextPageURL)

if __name__ == "__main__":
    title = "Hunch.net Blog"
    url = "https://hunch.net/"
    icon = "https://icon-library.com/images/h-icon/h-icon-18.jpg"
    dateFormat = "%m/%d/%Y"

    hunchnetblog_client = HunchNetBlogClient(title, url, icon, dateFormat)
    hunchnetblog_client.getResources(url)