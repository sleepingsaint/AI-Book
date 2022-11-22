import re
import requests
from bs4 import BeautifulSoup
from utils.python.aibook_client import AIBookClient 
from utils.python.decorators import tryExceptNone

class NeptuneAIBlogClient(AIBookClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, url, dateFormat)
        self.endpoint = "https://neptune.ai/wp-admin/admin-ajax.php"
        self.header = {"Content-Type": "application/x-www-form-urlencoded"}

        # form data for page requests
        self.wpq = {
            "page": 0,
            "pagename": "blog",
            "error": "",
            "m": "",
            "p": 0,
            "post_parent": "",
            "subpost": "",
            "subpost_id": "",
            "attachment": "",
            "attachment_id": 0,
            "name": "",
            "page_id": 0,
            "second": "",
            "minute": "",
            "hour": "",
            "day": 0,
            "monthnum": 0,
            "year": 0,
            "w": 0,
            "category_name": "",
            "tag": "",
            "cat": "",
            "tag_id": "",
            "author": "",
            "author_name": "",
            "feed": "",
            "tb": "",
            "paged": 0,
            "meta_key": "",
            "meta_value": "",
            "preview": "",
            "s": "",
            "sentence": "",
            "title": "",
            "fields": "",
            "menu_order": "",
            "embed": "",
            "category__in": [],
            "category__not_in": [],
            "category__and": [],
            "post__in": [],
            "post__not_in": [],
            "post_name__in": [],
            "tag__in": [],
            "tag__not_in": [],
            "tag__and": [],
            "tag_slug__in": [],
            "tag_slug__and": [],
            "post_parent__in": [],
            "post_parent__not_in": [],
            "author__in": [],
            "author__not_in": [],
            "ignore_sticky_posts": False,
            "suppress_filters": False,
            "cache_results": False,
            "update_post_term_cache": True,
            "lazy_load_term_meta": True,
            "update_post_meta_cache": True,
            "post_type": "",
            "posts_per_page": 12,
            "nopaging": False,
            "comments_per_page": 50,
            "no_found_rows": False,
            "order": "DESC"
        }

    @tryExceptNone
    def getTitle(self, tag):
        if tag is None:
            return None
        title_tag = tag.find("h2")
        return self.formatTitle(title_tag.text)
    
    @tryExceptNone
    def getURL(self, tag):
        if tag is None:
            return None
        
        url_tag = tag.find("a")
        url = url_tag["href"]
        return self.formatURL(url)

    @tryExceptNone
    def getPublishedOn(self, tag):
        if tag is None:
            return None

        url = self.getURL(tag)
        page = requests.get(url)
        
        soup = BeautifulSoup(page.content, "html.parser")
        meta_container = soup.find("div", {"class": "block-hero__meta"})
        meta_divs = meta_container.find_all("div")
        publishedOnDiv = meta_divs[-1].find("span")
        
        tmp = publishedOnDiv.text.strip().split(" ")
        day = tmp[0][0:2] if tmp[0][0:2].isnumeric() else tmp[0][0:1]
        
        month = tmp[1].replace(",", "").strip()
        year = tmp[-1].strip()
        return self.formatPublishedOn(f"{day} {month} {year}")

    @tryExceptNone
    def getAuthors(self, tag):
        if tag is None:
            return None

        author = tag.find("strong").text.replace("by", "").strip()
        return self.formatAuthors(author.split(','))

    @tryExceptNone
    def getTags(self, tag):
        if tag is None:
            return None

        return self.formatTags(None)

    def getData(self, page_num=1):
        data = {
            "action": "load_more_posts",
            "page": page_num,
            "wpq": self.wpq
        }
        return data

    @tryExceptNone
    def getNextPage(self, soup):
        pagination_container = soup.find("nav", {"class": "c-pagination"})
        next_div = pagination_container.find_all("div")[-1]
        next_url_tag = next_div.find("a")
        if next_url_tag is None:
            return None
        return next_url_tag['href']

    def getResources(self, page_num = 1):
        endpoint = f"{self.url}/page/{page_num}"
        page = requests.get(endpoint)
        soup = BeautifulSoup(page.content, "html.parser")
        posts = soup.find_all("article", {"class":"loop-post-item"})

        for post in posts:
            title = self.getTitle(post)
            url = self.getURL(post)
            
            if title is None or url is None:
                continue
            
            authors = self.getAuthors(post)
            publishedOn = self.getPublishedOn(post)
            tags = self.getTags(post)
            preview = self.getPreview(url)

            if not self.handleResource(title, url, authors, tags, publishedOn, preview.description, preview.image):
                return

        if self.getNextPage(soup) is not None:
            self.getResources(page_num = page_num + 1)

        

if __name__ == "__main__":
    title = "Neptune AI Blog"
    url = "https://neptune.ai/blog"
    dateFormat = "%d %B %Y"

    neptuneaiblog_client = NeptuneAIBlogClient(title, url, dateFormat)
    neptuneaiblog_client.getResources()