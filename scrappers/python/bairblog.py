import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class BAIRBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

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
            return self.formatAuthors(authors)
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

            if not self.db.resourceExists(title): 
                result = self.db.handleResource(self.source_id, title, url, authors, tags, publishedOn)
                if not result:
                    print(f"Resource cannot be created : {title}")
                    print(url, tags, authors, publishedOn, sep="\n")
            elif self.refetch:
                if not self.db.handleResource(self.source_id, title, url, authors, tags, publishedOn):
                    print(f"Resource cannot be updated : {title}")
                continue
            else:
                continue
                # return

        nextPageURL = self.nextPageUrl(soup)
        if nextPageURL is not None:
            self.getResources(nextPageURL)

if __name__ == "__main__":
    title = "BAIR Blog"
    url = "https://bair.berkeley.edu/blog/"
    icon = "https://bair.berkeley.edu/images/BAIR_Logo2.png"
    dateFormat = "%b %d, %Y"

    bairblog_client = BAIRBlogClient(title, url, icon, dateFormat)
    bairblog_client.getResources(url)