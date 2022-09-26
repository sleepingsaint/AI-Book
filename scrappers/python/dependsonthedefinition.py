from utils.python.resource_client import ResourceClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class DependsOnTheDefinitionClient(ResourceClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)

        options = Options()
        options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find_element(By.CLASS_NAME, "title")
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find_element(By.CLASS_NAME, "title")
            a = title_tag.find_element(By.TAG_NAME, "a")
            return self.formatURL(a.get_attribute("href"))
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find_element(By.CLASS_NAME, "date")
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
            tags = []
            tags_container = tag.find_element(By.CLASS_NAME, "tags")
            tag_elements = tags_container.find_elements(By.TAG_NAME, "a")
            for ele in tag_elements:
                tags.append(ele.text.replace("#", "").capitalize().strip())
            return self.formatTags(tags)
        except:
            return self.formatTags(None)

    def hasNextPage(self):
        try:
            container = self.driver.find_element(By.CLASS_NAME, "level-right")
            nextPageURL = container.find_element(By.TAG_NAME, "a").get_attribute("href")
            self.driver.get(nextPageURL)
            return True 
        except:
            return False 

    def getResources(self):
        prev = []
        while True:
            while True:
                try:
                    posts = self.driver.find_elements(By.TAG_NAME, "article")
                    if len(posts) > 0 and posts != prev:
                        break
                except:
                    pass

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
                    return

            if not self.hasNextPage():
                break
            prev = posts

if __name__ == "__main__":
    title = "Depends On The Definition Blog"
    url = "https://www.depends-on-the-definition.com/"
    icon = "https://d33wubrfki0l68.cloudfront.net/ad54dd6fbf992bd4b3c27fce860201ffbc943d01/0fdb7/header_icon_d.png"
    dateFormat = "%B %d, %Y"

    dependsonthedefinition_client = DependsOnTheDefinitionClient(title, url, dateFormat)
    dependsonthedefinition_client.getResources()
    dependsonthedefinition_client.driver.close()

    if dependsonthedefinition_client.new_source:
        dependsonthedefinition_client.discordSendSourceNotification(title, url)