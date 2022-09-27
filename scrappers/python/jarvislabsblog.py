import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class JarvisLabsAIBlogClient(ResourceClient):
    def __init__(self, title: str,  dateFormat: str) -> None:
        super().__init__(title, dateFormat)

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("h2", {"itemprop": "headline"})
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find("h2", {"itemprop": "headline"})
            a = title_tag.find("a")
            return self.formatURL("https://jarvislabs.ai" + a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find("time", {"itemprop": "datePublished"})
            return self.formatPublishedOn(publishedOn.text)
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            author_tag = tag.find("div", {"class": "avatar__name"})
            return self.formatAuthors(author_tag.text.split(","))
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None

        try:
            tags_container = tag.find("footer").find("ul")
            tag_elements = tags_container.find_all("a")
            tags = []
            for ele in tag_elements:
                tags.append(ele.text.strip())
                
            return self.formatTags(tags)
        except:
            return self.formatTags(None)

    def getResources(self, page_url):
        page = requests.get(page_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        
        posts = soup.find_all("article", {"itemprop": "blogPost"})

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

if __name__ == "__main__":
    title = "Jarvis Labs AI Blog"
    url = "https://jarvislabs.ai/blogs/"
    icon = "https://images.yourstory.com/cs/images/companies/dc15dab414c0-JarvisLogo512-1621092296781.png"
    dateFormat = "%B %d, %Y"

    jarvislabsaiblog_client = JarvisLabsAIBlogClient(title, dateFormat)
    jarvislabsaiblog_client.getResources(url)
    if jarvislabsaiblog_client.new_source:
        jarvislabsaiblog_client.sendSourceNotification(title, url)