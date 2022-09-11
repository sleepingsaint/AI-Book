import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class JarvisLabsAIBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

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
            return self.formatAuthors(author_tag.text)
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
                tags.append(ele.text)
                
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
    title = "Jarvis Labs AI Blog"
    url = "https://jarvislabs.ai/blogs/"
    icon = "https://images.yourstory.com/cs/images/companies/dc15dab414c0-JarvisLogo512-1621092296781.png"
    dateFormat = "%B %d, %Y"

    jarvislabsaiblog_client = JarvisLabsAIBlogClient(title, url, icon, dateFormat)
    jarvislabsaiblog_client.getResources(url)