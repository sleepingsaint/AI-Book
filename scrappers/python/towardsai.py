import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class TowardsAIBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)
        self.url = url

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("h3", {"class": "post-title"})
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find("h3", {"class": "post-title"})
            a = title_tag.find("a")
            return self.formatURL(a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find("div", {"class": "post-date"})
            return self.formatPublishedOn(publishedOn.text)
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            title_tag = tag.find("h3", {"class": "post-title"})
            a = title_tag.find("a")

            page = requests.get(a['href'])
            soup = BeautifulSoup(page.content, "html.parser")
            container = soup.find("h4", {"class": "medium-author"})

            author_tags = container.find_all("a")
            authors = []
            for author_tag in author_tags:
                authors.append(author_tag.text.strip())

            return self.formatAuthors(authors)
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None

        return self.formatTags(None)

    def nextPageUrl(self, soup):
        try:
            pagination_container = soup.find("ul", {"class": "page-pagination"})
            older_posts = pagination_container.find("a", {"class": "next"})
            if older_posts is not None and older_posts['href'] != "":
                return older_posts['href']
            return None
        except:
            return None

    def getResources(self):
        page_url = self.url
        while True:
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            container = soup.find("div", {"class": "page-main-content"})
            posts = container.find_all("div", {"class": "post"})

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
                        self.sendResourceNotification(url)
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


            page_url = self.nextPageUrl(soup)
            if page_url is None:
                break

if __name__ == "__main__":
    title = "Towards AI Blog"
    url = "https://towardsai.net/p"
    icon = "https://towardsai.net/wp-content/uploads/2019/05/towards-ai-square-circle-png.png"
    dateFormat = "%B %d, %Y"

    towardsaiblog_client = TowardsAIBlogClient(title, url, dateFormat)
    towardsaiblog_client.getResources()
    if towardsaiblog_client.new_source:
        towardsaiblog_client.sendSourceNotification(title, url)