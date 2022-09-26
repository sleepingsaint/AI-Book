import re
import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class HuggingFaceBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)
        self.url = url
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
            return self.formatURL("https://huggingface.co" + tag['href'])
        except:
            return None

    def convertDateStr(self, date_str):
        items = date_str.split(" ")
        if len(items) < 3:
            if (items[0][0].isalpha()):
                month, year = items
                month = self.months.index(month[:3]) + 1
                day = 1
            elif (items[0][0].isnumeric()):
                day, year = items
                day = re.sub("\D", "", day)
                month = 1
                year = year
        else:
            month, day, year = items
            month = self.months.index(month[:3]) + 1
            day = re.sub("\D", "", day)
            year = year
        
        return f"{day} {month} {year}"

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            meta = tag.find("p")
            spans = meta.find_all("span")
            if len(spans) > 1:
                publishedOn = spans[1]
            else:
                return None
            date_str = self.convertDateStr(publishedOn.text)
            return self.formatPublishedOn(date_str)
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            meta = tag.find("p")
            author = meta.find("a")
            return self.formatAuthors(author.text.split(","))
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None

        return self.formatTags(None)
    
    def nextPageUrl(self, soup):
        try:
            pagination_container = soup.find("nav", {"role": "navigation"})
            ul = pagination_container.find("ul")
            li = ul.findChildren("li")[-1]
            a = li.find("a")
            if a['href'] != "":
                return "https://huggingface.co" + a['href']
            return None
        except Exception as e:
            print(e)
            return None

    def getResources(self, initial_url):

        page_url = initial_url
        while True:
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            
            container = soup.find("main").find("div").find("div").findChildren("div", recursive=False)[-1]
            posts = container.findChildren("a", recursive=False)

            if page_url != self.url and len(posts) > 0:
                posts = posts[1:]

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
                        self.discordSendResourceNotification(url)
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
                    print("Something went wrong!!")
                    return
            
            nextPageURL = self.nextPageUrl(soup)
            if nextPageURL is None:
                break
            page_url = nextPageURL

if __name__ == "__main__":
    title = "Huggingface Blog"
    url = "https://huggingface.co/blog"
    icon = "https://avatars.githubusercontent.com/u/25720743"
    dateFormat = "%d %m %Y"

    huggingfaceblog_client = HuggingFaceBlogClient(title, url, dateFormat)
    huggingfaceblog_client.getResources(url)
    if huggingfaceblog_client.new_source:
        huggingfaceblog_client.discordSendSourceNotification(title, url)