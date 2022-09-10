import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class KoaningIOBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("h2")
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            return self.formatURL(self.url + tag['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find("div", {"class": "publishedDate"})
            publishedOn = publishedOn.text.replace(".", "").replace(",", "").strip()
            month, date, year = publishedOn.split(" ")
            month = month[:3]
            month = self.months.index(month) + 1

            return self.formatPublishedOn(f"{date} {month} {year}")
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            author_tags = tag.find_all("div", {"class": "dt-author"})
            authors = []
            for author_tag in author_tags:
                authors.append(author_tag.text)
            return self.formatAuthors(authors)
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None
        return self.formatTags(None)

    def getResources(self, page_url):
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        posts = soup.find_all("a", {"class": "post-preview"})

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
    title = "Koaning.io Blog"
    url = "https://koaning.io/"
    icon = "https://cdn-icons-png.flaticon.com/512/625/625187.png"
    dateFormat = "%d %m %Y"

    koaningioblog_client = KoaningIOBlogClient(title, url, icon, dateFormat)
    koaningioblog_client.getResources(url)