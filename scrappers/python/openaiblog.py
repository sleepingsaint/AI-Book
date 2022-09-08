import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class OpenAIClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)
        
    def getTitle(self, tag):
        if tag is None:
            return None

        try:
            a = tag.find("h5").find("a")
            return self.formatTitle(a.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None

        try:
            a = tag.find("h5").find("a")
            return self.formatURL("https://openai.com" + a["href"])
        except:
            return None
    
    def getAuthors(self, tag):
        return self.formatAuthors(None) 

    def getPublishedOn(self, tag):
        if tag is None:
            return None
        try:
            time = tag.find("time")
            return self.formatPublishedOn(time.text)
        except:
            return None

    def getTags(self, tag=None):
        if tag is None:
            return self.formatTags(None)
        try:
            ul = tag.find("ul")
            tag_elements = ul.findAll("a")
            tags = []
            for ele in tag_elements:
                tags.append(ele.text)
            return self.formatTags(tags)
        except:
            return self.formatTags(None) 

    def getResources(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        posts = soup.find_all("div", class_="post-card-full")

        for post in posts:
            title = self.getTitle(post)
            url = self.getURL(post)
            if title is None or url is None:
                continue

            publishedOn = self.getPublishedOn(post)
            authors = self.getAuthors(post)
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
                return


if __name__ == "__main__":
    title = "OpenAI Blog"
    url = "https://openai.com/blog/"
    icon = "https://www.pngitem.com/pimgs/m/66-668806_openai-logo-openai-logo-elon-musk-hd-png.png"
    dateFormat = "%B %d, %Y"

    openai_client = OpenAIClient(title, url, icon, dateFormat)
    openai_client.getResources(url)