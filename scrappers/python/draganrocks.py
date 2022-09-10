import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class DraganRocksBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

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

if __name__ == "__main__":
    title = "Dragan.rocks Blog"
    url = "https://dragan.rocks"
    icon = "https://cdn.iconscout.com/icon/free/png-256/d-character-alphabet-letter-32851.png"
    dateFormat = "%B %d, %Y"

    draganrocksblog_client = DraganRocksBlogClient(title, url, icon, dateFormat)
    draganrocksblog_client.getResources(url)