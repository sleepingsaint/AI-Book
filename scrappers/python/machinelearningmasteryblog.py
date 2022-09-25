from selenium import webdriver
from utils.python.resource_client import ResourceClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class MachineLearningMasteryBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)
        
        options = Options()
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)

        # removing the cookie btn

    def getTitle(self, tag):
        if tag is None:
            return None

        try:
            title = tag.find_element(By.CLASS_NAME, "entry-title")
            return self.formatTitle(title.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None

        try:
            title = tag.find_element(By.CLASS_NAME, "entry-title")
            a = title.find_element(By.TAG_NAME, "a")
            return self.formatURL(a.get_attribute("href"))
        except:
            return None
    
    def getAuthors(self, tag):
        if tag is None:
            return None
        try:
            meta = tag.find_element(By.CLASS_NAME, "post-meta")
            author_tag = meta.find_element(By.CLASS_NAME, "author")
            return self.formatAuthors(author_tag.text.split(','))
        except:
            return None
    
    def getPublishedOn(self, tag):
        if tag is None:
            return None
        try:
            meta = tag.find_element(By.CLASS_NAME, "post-meta")
            publishedOn = meta.find_element(By.CLASS_NAME, "date")
            return self.formatPublishedOn(publishedOn.text)
        except:
            return None

    def getTags(self, tag=None):
        if tag is None:
            return self.formatTags(None)
        try:
            meta = tag.find_element(By.CLASS_NAME, "post-meta")

            tags = []
            categories_tag = meta.find_element(By.CLASS_NAME, "categories")
            tags_elements = categories_tag.find_elements(By.TAG_NAME, "a")
            for ele in tags_elements:
                tags.append(ele.text.strip())

            return self.formatTags(tags)
        except:
            return self.formatTags(None) 

    def hasNextPage(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "next").click()
            return True 
        except:
            return False

    def getResources(self):
        prev = []
        while True: 
            while True:
                try:
                    articles = self.driver.find_elements(By.CLASS_NAME, "post")
                    if len(articles) > 0 and articles != prev:
                        break
                except:
                    pass

            for article in articles:
                title = self.getTitle(article)
                url = self.getURL(article)

                if title is None or url is None:
                    continue

                authors = self.getAuthors(article)
                tags = self.getTags(article)
                publishedOn = self.getPublishedOn(article)
                
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
                    return

            if not self.hasNextPage():
                break
            prev = articles

if __name__ == "__main__":
    title = "Machine Learning Mastery Blog"
    url = "https://machinelearningmastery.com/blog/"
    icon = "https://machinelearningmastery.com/wp-content/uploads/2016/09/cropped-icon.png"
    dateFormat = "%B %d, %Y"

    machinelearningmasteryblog_client = MachineLearningMasteryBlogClient(title, url, dateFormat)
    machinelearningmasteryblog_client.getResources()
    machinelearningmasteryblog_client.driver.close()
