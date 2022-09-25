import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class OpenAIClient(ResourceClient):
    def __init__(self, title: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)
        
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
                tags.append(ele.text.strip())
            return self.formatTags(tags)
        except:
            return self.formatTags(None) 

    def getResources(self, initial_url):
        url = initial_url
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
                print("Helllo")
                return


if __name__ == "__main__":
    title = "OpenAI Blog"
    url = "https://openai.com/blog/"
    icon = "https://www.pngitem.com/pimgs/m/66-668806_openai-logo-openai-logo-elon-musk-hd-png.png"
    dateFormat = "%B %d, %Y"

    openai_client = OpenAIClient(title, dateFormat)
    openai_client.getResources(url)