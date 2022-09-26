import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class DraganRocksBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)
        self.url = url

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("a")
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find("a")
            return self.formatURL(self.url + title_tag['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            span = tag.find("span")
            return self.formatPublishedOn(span.text)
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

    def getResources(self, page_url):
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        posts = soup.find_all("li", {"class": "listing"})
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
                print("Something went wrong")
                return

if __name__ == "__main__":
    title = "Dragan.rocks Blog"
    url = "https://dragan.rocks"
    icon = "https://cdn.iconscout.com/icon/free/png-256/d-character-alphabet-letter-32851.png"
    dateFormat = "%B %d, %Y"

    draganrocksblog_client = DraganRocksBlogClient(title, url, dateFormat)
    draganrocksblog_client.getResources(url)
    if draganrocksblog_client.new_source:
        draganrocksblog_client.discordSendSourceNotification(title, url)
