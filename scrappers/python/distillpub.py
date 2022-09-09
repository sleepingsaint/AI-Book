import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class DistillPubBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

        # to convert the distill.pub date format to iso format
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title = tag.find("h2", class_="title")
            return self.formatTitle(title.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            a = tag.findChildren("a", recursive=False)[0]
            return self.formatURL(self.url + a['href'])
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None
        try:
            publishedOn = tag.find("div", class_="publishedDate").text
            month = self.months.index(publishedOn[:3]) + 1
            date_idx = publishedOn.find(" ")
            return self.formatPublishedOn(str(month) + " " + publishedOn[date_idx:])
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            authors_tag = tag.find("p", class_="authors")
            return self.formatAuthors(authors_tag.text)
        except:
            return None

    def getTags(self, tag):
        if tag is None:
            return None

        try:
            tags_container = tag.find("div", class_="tags")
            tag_spans = tags_container.find_all("span")
            tags = []
            for span in tag_spans:
                tags.append(span.text)
            return self.formatTags(tags)
        except:
            return None
    
    def getResources(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        posts = soup.find_all("div", class_="post-preview")
        
        for post in posts:
            title = self.getTitle(post)
            url = self.getURL(post)

            if title is None or url is None:
                continue
            
            authors = self.getAuthors(post)
            tags = self.getTags(post)
            publishedOn = self.getPublishedOn(post)
            
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
    title = "Distill Pub Blog"
    url = "https://distill.pub/"
    icon = "https://pbs.twimg.com/profile_images/1217512741956489216/VMIw85Xe_400x400.jpg"
    dateFormat = "%m %d, %Y"

    distillpubblog_client = DistillPubBlogClient(title, url, icon, dateFormat)
    distillpubblog_client.getResources()