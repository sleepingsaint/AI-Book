import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class HunchNetBlogClient(ResourceClient):
    def __init__(self, title: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)

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

    def getResources(self, initial_url):
        page_url = initial_url
        while True:
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

                resourceExists = self.db.resourceExists(url)
                if not resourceExists:
                    result = self.db.addResource(title=title, url=url, publishedOn=publishedOn, authors=authors, tags=tags, source=self.source)
                    if not result:
                        print(f"Resource cannot be created : {title}")
                        print(url, tags, authors, publishedOn, sep="\n")
                    elif not self.refetch:
                        self.discordSendResourceNotification(url)
                elif self.refetch:
                    result = self.db.updateResource(page_id=resourceExists, title=title, url=url, publishedOn=publishedOn, authors=authors, tags=tags, source=self.source)
                    if not result:
                        print(f"Resource cannot be updated : {title}")
                    continue
                elif self.delete:
                    result = self.db.deleteResource(page_id=resourceExists)
                    if not result:
                        print(f"Resource cannot be deleted : {title}")
                    continue
                else:
                    return

            nextPageURL = self.nextPageUrl(soup)
            if nextPageURL is None:
                break
            page_url = nextPageURL

if __name__ == "__main__":
    title = "Hunch.net Blog"
    url = "https://hunch.net/"
    icon = "https://icon-library.com/images/h-icon/h-icon-18.jpg"
    dateFormat = "%m/%d/%Y"

    hunchnetblog_client = HunchNetBlogClient(title, dateFormat)
    hunchnetblog_client.getResources(url)
    if hunchnetblog_client.new_source:
        hunchnetblog_client.discordSendSourceNotification(title, url)