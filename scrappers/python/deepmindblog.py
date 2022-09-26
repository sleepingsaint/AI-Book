import time
from selenium import webdriver
from utils.python.resource_client import ResourceClient
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class DeepmindBlogClient(ResourceClient):
    def __init__(self, title: str, dateFormat: str) -> None:
        super().__init__(title, dateFormat)
        
        options = Options()
        options.add_argument("--headless")
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driver.get(url)

        # removing the cookie btn
        cookie_bar_btn = self.driver.find_element(By.CLASS_NAME, "cookieBarConsentButton")
        cookie_bar_btn.click()

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
            return self.formatAuthors(a.text.split(','))
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
            self.driver.find_element(By.CLASS_NAME, "w-pagination-next").click()
            return True 
        except:
            return False
    
    def getBannerPost(self):
        banner_post = self.driver.find_element(By.CLASS_NAME, "c_banner__blog__card")

        title = banner_post.find_element(By.CLASS_NAME, "c_banner__blog__card__title").text
        tags = banner_post.find_element(By.CLASS_NAME, "c_banner__blog__card__category").text
        publishedOn = banner_post.find_element(By.CLASS_NAME, "c_banner__blog__card__meta").text
        url = banner_post.find_element(By.CLASS_NAME, "c_banner__blog__card__link").get_attribute('href')

        title = self.formatTitle(title)
        url = self.formatURL(url)

        if title is None or url is None:
            return

        authors = self.formatAuthors(None)
        publishedOn = self.formatPublishedOn(publishedOn)
        tags = self.formatTags(tags)

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
        elif self.delete:
            result = self.db.deleteResource(page_id=resourceExists)
            if not result:
                print(f"Resource cannot be deleted : {title}")
        else:
            return
    
    def getContentPosts(self):
        posts = self.driver.find_elements(By.CLASS_NAME, "c_content_cards__blog_card")
        for content_post in posts:
            meta_container = content_post.find_element(By.CLASS_NAME, "c_content_cards__blog_card__text")

            title = meta_container.find_element(By.CLASS_NAME, "c_content_cards__blog_card__title").text
            tags = meta_container.find_element(By.CLASS_NAME, "c_content_cards__list__category").text
            publishedOn = meta_container.find_elements(By.TAG_NAME, "div")[-1].text
            url = content_post.find_element(By.CLASS_NAME, "c_blog_cards__link").get_attribute('href')
            
            title = self.formatTitle(title)
            url = self.formatURL(url)

            if title is None or url is None:
                return

            authors = self.formatAuthors(None)
            publishedOn = self.formatPublishedOn(publishedOn)
            tags = self.formatTags(tags)

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

    def getResources(self, page_num=0):
        time.sleep(1)

        if page_num == 0:
            self.getBannerPost()
            self.getContentPosts() 

        container = self.driver.find_element(By.CLASS_NAME, "bg-grey-50")
        container = container.find_element(By.CLASS_NAME, "w-dyn-list").find_element(By.CLASS_NAME, "w-dyn-items")
        posts = container.find_elements(By.XPATH, "div[@role = 'listitem']")
        for post in posts:
            tags, title, date = post.text.split("\n")
            url = post.find_element(By.CLASS_NAME, "c_card_list__link").get_attribute("href")

            title = self.formatTitle(title)
            url = self.formatURL(url)

            if title is None or url is None:
                continue

            authors = self.formatAuthors(None)
            publishedOn = self.formatPublishedOn(date)
            tags = self.formatTags(tags)

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

        if self.hasNextPage():
            self.getResources(page_num=page_num + 1)


if __name__ == "__main__":
    title = "Deepmind Blog"
    url = "https://www.deepmind.com/blog"
    icon = "https://avatars.githubusercontent.com/u/8596759"
    dateFormat = "%B %d, %Y"

    deepmindblog_client = DeepmindBlogClient(title, dateFormat)
    deepmindblog_client.getResources()
    deepmindblog_client.driver.close()

    if deepmindblog_client.new_source:
        deepmindblog_client.discordSendSourceNotification(title, url)