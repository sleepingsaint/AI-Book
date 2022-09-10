from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from utils.python.resource_client import ResourceClient

class NeuralMagicBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

        options = Options()
        # options.add_argument("--headless")
        # options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)

        # declining cookies
        self.driver.find_element(By.ID, "hs-eu-decline-button").click()

    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find_element(By.CLASS_NAME, "entry-title")
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            title_tag = tag.find_element(By.CLASS_NAME, "entry-title")
            a = title_tag.find_element(By.TAG_NAME, "a")
            return self.formatURL(a.get_attribute("href"))
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            publishedOn = tag.find_element(By.CLASS_NAME, "entry-date")
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

        return self.formatTags(None)

    def hasNextPage(self):
        try:
            pagination = self.driver.find_element(By.CLASS_NAME, "pagination")
            next_page_btn = pagination.find_element(By.CLASS_NAME, "nav-next-text")
            next_page_btn.click()
            return True 
        except:
            return False 

    def getResources(self):
        prev = []
        while True:
            while True:
                try:
                    posts = self.driver.find_elements(By.CLASS_NAME, "post")
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
            if not self.hasNextPage():
                break
            prev = posts

if __name__ == "__main__":
    title = "Neural Magic Blog"
    url = "https://neuralmagic.com/blog/"
    icon = "https://docs.neuralmagic.com/_static/icon-neuralmagic.png"
    dateFormat = "%m/%d/%y"

    neuralmagicblog_client = NeuralMagicBlogClient(title, url, icon, dateFormat)
    neuralmagicblog_client.getResources()
    # neuralmagicblog_client.driver.close()