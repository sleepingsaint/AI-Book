import re
import requests
from bs4 import BeautifulSoup
from utils.python.resource_client import ResourceClient

class NeptuneAIBlogClient(ResourceClient):
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        super().__init__(title, url, icon, dateFormat)

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
    def getTitle(self, tag):
        if tag is None:
            return None
        try:
            title_tag = tag.find("h4")
            return self.formatTitle(title_tag.text)
        except:
            return None
    
    def getURL(self, tag):
        if tag is None:
            return None
        
        try:
            url = tag["href"]
            return self.formatURL(url)
        except:
            return None

    def getPublishedOn(self, tag):
        if tag is None:
            return None

        try:
            url = tag['href']
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            ul = soup.find("ul", {"class": "article__info"})
            li = ul.find_all("li")[-1]
            
            month, day, year = li.text.replace("Updated", "").strip().split(" ")
            day = re.sub("\D", "", day)
            
            return self.formatPublishedOn(f"{day} {month} {year}")
        except:
            return None

    def getAuthors(self, tag):
        if tag is None:
            return None

        try:
            author_tag = tag.find("p", {"class": "author"})
            author = author_tag.find("strong").text.replace("by", "").strip()
            return self.formatAuthors(author)
        except:
            return None

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

    def getNextPage(self, page_num=1):
        try:
            data = self.getData(page_num)
            resp = requests.post(self.endpoint, data=data, headers=self.header)
            if resp.status_code == 200:
                return resp.content
            return None 
        except:
            return None 

    def getResources(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        posts = soup.find_all("a", {"class":"single-new-post"})

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

        page_num = 1
        while True:
            content = self.getNextPage(page_num)
            if content is None:
                break

            print(page_num)
            soup = BeautifulSoup(content, "html.parser")
            posts = soup.find_all("a", {"class": "single-new-post"})

            if len(posts) == 0:
                break

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

            page_num += 1

if __name__ == "__main__":
    title = "Neptune AI Blog"
    url = "https://neptune.ai/blog"
    icon = "https://avatars.githubusercontent.com/u/30523139?s=280&v=4"
    dateFormat = "%d %B %Y"

    neptuneaiblog_client = NeptuneAIBlogClient(title, url, icon, dateFormat)
    neptuneaiblog_client.getResources()