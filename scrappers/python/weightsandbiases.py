import re 
from utils.python.resource_client import ResourceClient
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from datetime import date

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

class WeightsAndBiasesClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)
        
        today_date = date.today()
        self.day = today_date.day
        self.month = today_date.month
        self.year = today_date.year
        self.months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(url)
        
    def getTitle(self, tag):
        if tag is None or tag.find_element(By.TAG_NAME, "div") is None:
            return None
        return self.formatTitle(tag.find_element(By.TAG_NAME, "div").get_attribute("innerHTML"))
    
    def getURL(self, tag):
        if tag is None or tag.get_attribute('href') is None:
            return None
        return self.formatURL(tag.get_attribute('href'))
    
    def getAuthors(self, tag):
        if tag is None or tag.find_element(By.TAG_NAME, "a") is None:
            return self.formatAuthors(None)
        
        links = tag.find_elements(By.TAG_NAME, "a")
        authors = []
        for link in links:
            authors.append(link.get_attribute("innerHTML"))
        return self.formatAuthors(authors) 
    
    def getDate(self, day_str, month_str):
        month = self.months.index(month_str) + 1
        day = int(day_str)

        if month > self.month:
            self.day = day
            self.month = month
            self.year = self.year - 1
        elif month == self.month:
            if day > self.day:
                self.day = day
                self.month = month
                self.year = self.year - 1
        else:
            self.day = day
            self.month = month
        
        return f"{self.day} {self.months[self.month - 1]} {self.year}"

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        text = tag.text
        
        for link in tag.find_elements(By.TAG_NAME, "a"):
            text = text.replace(link.text, "")
        for span in tag.find_elements(By.TAG_NAME, "span"):
            text = text.replace(span.text, "")
        
        text = text.replace(',', '').strip()
        
        month = text[0:3].strip()
        day = text[4:6].strip()

        date_string = self.getDate(day, month)
        return self.formatPublishedOn(date_string)

    def getTags(self, tag):
        if tag is None or tag.find_element(By.TAG_NAME, "span") is None:
            return self.formatTags(None)

        spans = tag.find_elements(By.TAG_NAME, "span")
        tags = []
        for span in spans:
            tags.append(span.get_attribute("innerHTML"))
        return self.formatTags(tags) 

    def hasNextPage(self):
        nav_bar_cls = "dlvKMM"
        nav_bar = self.driver.find_element(By.CLASS_NAME, nav_bar_cls)
        next_btn = nav_bar.find_elements(By.TAG_NAME, "a")[-1]
        if next_btn.get_attribute('disabled') is None:
            next_btn.click()
            return True
        return False

    def getResources(self, page_num=0):
        while True:
            try:
                new_posts = self.driver.find_elements(By.CLASS_NAME, "elPKvX")
                if len(new_posts) > 0: 
                    break
            except NoSuchElementException:
                pass
        
        if page_num > 0:
            new_posts = new_posts[4:]

        for post in new_posts:
            a = post.find_element(By.TAG_NAME, "a")
            title = self.getTitle(a.find_element(By.TAG_NAME, "div"))
            url = self.getURL(a)
            
            if title is None or url is None:
                continue
            meta_container = a.find_element(By.TAG_NAME, "div").find_elements(By.TAG_NAME, "div")[1]
            
            authors = self.getAuthors(meta_container)
            tags = self.getTags(meta_container)
            publishedOn = self.getPublishedOn(meta_container)
            
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

        if self.hasNextPage():
            page_num = page_num + 1
            self.getResources(page_num)


if __name__ == "__main__":
    title = "Weights And Biases Blog"
    url = "https://wandb.ai/fully-connected"
    icon = "https://1039519455-files.gitbook.io/~/files/v0/b/gitbook-legacy-files/o/spaces%2F-Lqya5RvLedGEWPhtkjU%2Favatar.png?generation=1570983771045343&alt=media"
    dateFormat = "%d %b %Y"

    weights_and_biases_resource_client = WeightsAndBiasesClient(title, url, icon, dateFormat)
    weights_and_biases_resource_client.getResources()
