import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class AmazonScienceBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("div", {"class": "PromoF-title"})
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find("div", {"class": "PromoF-title"})
            a = title_tag.find("a")
            return self.formatURL(a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find("div", {"class": "PromoF-date"})
            return self.formatPublishedOn(publishedOn.text)
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            authors = tag.find("div", {"class": "PromoF-authors"})
            return self.formatAuthors(authors.text)
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None

        try:
            tags = tag.find("div", {"class": "PromoF-category"})
            return self.formatTags(tags.text)
        except:
            return self.formatTags(None)

    def nextPageUrl(self, soup):
        try:
            pagination_container = soup.find("div", {"class": "SearchResultsModule-nextPage"})
            older_posts = pagination_container.find("a")
            if older_posts is not None:
                return older_posts['href']
            return None
        except:
            return None

    def getResources(self, page_url):
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        posts = soup.find_all("li", {"class": "SearchResultsModule-results-item"})
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
    title = "Amazon Science Blog"
    url = "https://www.amazon.science/blog"
    icon = "https://assets.amazon.science/dims4/default/2e80245/2147483647/strip/true/crop/1120x630+40+0/resize/1200x675!/quality/90/?url=http%3A%2F%2Famazon-topics-brightspot.s3.amazonaws.com%2Fscience%2F32%2F80%2Fc230480c4f60a534bc077755bae7%2Famazon-science-og-image-squid.png"
    dateFormat = "%B %d, %Y"

    amazonscienceblog_client = AmazonScienceBlogClient(title, url, icon, dateFormat)
    amazonscienceblog_client.getResources(url)