import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class MLAtCMUBlogClient(ResourceClient):
    def __init__(self, title: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            header = tag.find("div", {"class": "post-header"})
            title_tag = header.find("h2")
            if title_tag is None:
                title_tag = header.find("h3")
            
            if title_tag is None:
                return self.formatTitle(None)
            
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            header = tag.find("div", {"class": "post-header"})
            title_tag = header.find("h2")

            if title_tag is None:
                title_tag = header.find("h3")
            
            if title_tag is None:
                return self.formatURL(None)
            
            a = title_tag.find("a")
            return self.formatURL(a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            meta = tag.find("div", {"class": "post-info"})
            publishedOn = meta.find("span", {"class": "date"})
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

        try:
            header = tag.find("div", {"class": "post-header"})
            category = header.find("span", {"class": "category-post"})
            tag_elements = category.find_all("a")
            tags = []
            for ele in tag_elements:
                tags.append(ele.text.capitalize().strip())
            return self.formatTags(tags)
        except:
            return self.formatTags(None)

    def nextPageUrl(self, soup):
        try:
            pagination_container = soup.find("div", {"class": "pagination"})
            older_posts = pagination_container.find("div", {"class": "older"})
            a = older_posts.find("a")
            if a is not None:
                return a['href']
            return None
        except:
            return None

    def getResources(self, initial_url):
        page_url = initial_url
        while True:
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            container = soup.find("div", {"class": "post-list"})
            posts = container.find_all("aside", {"class": "post"})

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
            if nextPageURL is None:
                break

            page_url = nextPageURL

if __name__ == "__main__":
    title = "ML@CMU Blog"
    url = "https://blog.ml.cmu.edu/"
    icon = "https://pbs.twimg.com/profile_images/1233560739710984197/wMfC5fXd_400x400.jpg"
    dateFormat = "%B %d, %Y"

    mlatcmublog_client = MLAtCMUBlogClient(title, dateFormat)
    mlatcmublog_client.getResources(url)