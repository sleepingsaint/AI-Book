import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class GoogleAIClient(ResourceClient):
    def __init__(self, title: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)

    def formatAuthors(self, authors: str) -> str:
        tmp = super().formatAuthors(authors)
        if tmp is None:
            return tmp
        authors = tmp.replace("Posted by", "").strip().split(",")
        return list(map(lambda x: x.strip(), authors))
    
    def getTitle(self, tag):
        if tag is None or tag.text is None:
            return None 
        return self.formatTitle(tag.text)
    
    def getURL(self, tag):
        if tag is None or tag['href'] is None:
            return None
        return self.formatURL(tag['href'])
    
    def getPublishedOn(self, tag):
        publishedOnTag = tag.find('span', class_="publishdate")
        if publishedOnTag is None or publishedOnTag.text is None:
            return None
        return self.formatPublishedOn(publishedOnTag.text)

    def getAuthors(self, tag):
        authorsTag = tag.find('span', class_='byline-author')
        if authorsTag is None or authorsTag.text is None:
            return None
        return self.formatAuthors(authorsTag.text)

    def getResources(self, initial_url):
        page_url = initial_url
        while True:
            page = requests.get(page_url)
            soup = BeautifulSoup(page.content, 'html.parser')
            posts = soup.find_all("div", class_="post")

            for post in posts:
                titleTag = post.find("h2", class_="title").find("a", href=True)

                # extracting data
                title = self.getTitle(titleTag)
                url = self.getURL(titleTag)
                publishedOn = self.getPublishedOn(post)
                authors = self.getAuthors(post)
                tags = self.formatTags(None)
                
                if title is None or url is None:
                    continue
                    
                url = url.replace("http://", "https://")

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
                    return

            olderPostsLink = soup.find("a", class_="blog-pager-older-link", href=True)

            if(olderPostsLink is None):
                return
            page_url = olderPostsLink['href']

if __name__ == "__main__":
    title = "Google AI Blog"
    url = "https://ai.googleblog.com/"
    icon = "https://cdn.worldvectorlogo.com/logos/google-ai-1.svg"
    dateFormat = "%A, %B %d, %Y"

    googleaiblog_client = GoogleAIClient(title, dateFormat)
    googleaiblog_client.getResources(url)
    if googleaiblog_client.new_source:
        googleaiblog_client.discordSendSourceNotification(title, url)