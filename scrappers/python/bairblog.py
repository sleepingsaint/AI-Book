import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class BAIRBlogClient(ResourceClient):
    def __init__(self, title: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("h1", class_="post-title")
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            url = tag.find("a", class_="post-link")['href']
            return self.formatURL("https://bair.berkeley.edu" + url)
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            meta_tags = tag.find_all("span", class_="post-meta")
            publishedOn = meta_tags[1].text
            return self.formatPublishedOn(publishedOn)
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            meta_tags = tag.find_all("span", class_="post-meta")
            authors = meta_tags[0].text
            return self.formatAuthors(authors.split(','))
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None
        return self.formatTags(None)

    def nextPageUrl(self, soup):
        try:
            older = soup.find("div", class_="right")
            a = older.find("a", class_="pagination-item")
            url = "https://bair.berkeley.edu" + a['href']
            return url 
        except:
            return None

    def getResources(self, page_url):

        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        container = soup.find("div", class_="posts")
        posts = container.findChildren("div", recursive=False) 

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
        if nextPageURL is not None:
            self.getResources(nextPageURL)

if __name__ == "__main__":
    title = "BAIR Blog"
    url = "https://bair.berkeley.edu/blog/"
    icon = "https://bair.berkeley.edu/images/BAIR_Logo2.png"
    dateFormat = "%b %d, %Y"

    bairblog_client = BAIRBlogClient(title, dateFormat)
    bairblog_client.getResources(url)