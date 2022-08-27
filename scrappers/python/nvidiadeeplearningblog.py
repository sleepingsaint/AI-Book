import re 
from utils.python.resource_client import ResourceClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

class NvidiaDeepLearningBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

        options = Options()
        options.add_argument("--headless")

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.driver.get(url)

        post_container_xpath = "/html/body/div[1]/div[2]/div/div/main/div/div[2]/div[1]"
        while True:
            try:
                self.driver.find_element(By.XPATH, post_container_xpath)
                print("Page Loaded")
                break
            except NoSuchElementException:
                pass


        self.container = self.driver.find_element(By.XPATH, post_container_xpath)
        self.actions = ActionChains(self.driver)

        exit_cookies = self.driver.find_element(By.ID, "exit")
        if exit_cookies is not None:
            exit_cookies.click() 
        
    def getTitle(self, tag):
        if tag is None or tag.get_attribute('innerHTML') is None:
            return None 
        return self.formatTitle(tag.get_attribute('innerHTML'))
    
    def getURL(self, tag):
        if tag is None or tag.get_attribute('href') is None:
            return None
        return self.formatURL(tag.get_attribute('href'))
    
    def getPublishedOn(self, url):
        publishedOnDate = re.findall("/[0-9]+/[0-9/+/[0-9]+/", url)        
        if len(publishedOnDate) == 0:
            return None
        return self.formatPublishedOn(publishedOnDate[0])

    def getResources(self, num_posts=0):
        print(num_posts)
        while True:
            try:
                if len(self.container.find_elements(By.TAG_NAME, "article")) > num_posts:
                    break
            except:
                pass
        
        posts = self.container.find_elements(By.TAG_NAME, "article")

        for post in posts[num_posts:]:
            title_tag = post.find_element(By.CLASS_NAME, "entry-title-text")
            
            title = self.getTitle(title_tag)
            url = self.getURL(title_tag)

            if title is None or url is None:
                continue
            
            publishedOn = self.getPublishedOn(url) 
            authors = None
            tags = None
            
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
        
        num_posts = len(posts)
        load_more_btn = self.driver.find_element(By.CLASS_NAME, 'load-more-wrapper')
        if load_more_btn is not None:
            self.actions.move_to_element(load_more_btn).perform()
            load_more_btn.click()
            self.getResources(num_posts) 

if __name__ == "__main__":
    title = "Nvidia Deep Learning Blog"
    url = "https://blogs.nvidia.com/blog/category/deep-learning/"
    icon = "https://cdn-icons-png.flaticon.com/512/732/732230.png"
    dateFormat = "/%Y/%m/%d/"

    nvidia_deeplearning_blog_client = NvidiaDeepLearningBlogClient(title, url, icon, dateFormat)
    nvidia_deeplearning_blog_client.getResources()

