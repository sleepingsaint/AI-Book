from selenium import webdriver
from utils.python.resource_client import ResourceClient
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class MarkTechPostClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)
        
        options = Options()
        options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)
        
    def getTitle(self, tag):
        if tag is None:
            return None

        try:
            h3 = tag.find_element(By.TAG_NAME, "h3")
            a = h3.find_element(By.TAG_NAME, "a")
            return self.formatTitle(a.get_attribute("title"))
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None

        try:
            h3 = tag.find_element(By.TAG_NAME, "h3")
            a = h3.find_element(By.TAG_NAME, "a")
            return self.formatURL(a.get_attribute("href"))
        except:
            return None
    
    def getAuthors(self, tag):
        if tag is None:
            return None
        try:
            span = tag.find_element(By.CLASS_NAME, "td-post-author-name")
            a = span.find_element(By.TAG_NAME, "a")
            return self.formatAuthors(a.text)
        except:
            return None
    
    def getPublishedOn(self, tag):
        if tag is None:
            return None
        try:
            span = tag.find_element(By.CLASS_NAME, "td-post-date")
            return self.formatPublishedOn(span.text)
        except:
            return None

    def getTags(self, tag=None):
        if tag is None:
            return self.formatTags(None)
        return self.formatTags(None) 

    def hasNextPage(self):
        try:
            next_page_btn = self.driver.find_element(By.CSS_SELECTOR, "a[aria-label='next-page']")
            next_page_btn.click()
            return True
        except:
            return False

    def getResources(self, prev=[]):
        while True:
            try:
                posts = self.driver.find_elements(By.CLASS_NAME, "td-block-span4")
                if posts != prev:
                    break
            except NoSuchElementException:
                pass

        for post in posts:
            title = self.getTitle(post)
            url = self.getURL(post)
            
            if title is None or url is None:
                continue

            authors = self.getAuthors(post)
            publishedOn = self.getPublishedOn(post)
            tags = self.getTags(None)

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

        if self.hasNextPage():
            self.getResources(posts)

if __name__ == "__main__":
    title = "MarkTechPost"
    url = "https://www.marktechpost.com/category/technology/"
    icon = "https://pbs.twimg.com/profile_images/994114664874180608/tD0vcytP_400x400.jpg"
    dateFormat = "%B %d, %Y"

    markTechPost_client = MarkTechPostClient(title, url, icon, dateFormat)
    markTechPost_client.getResources()
