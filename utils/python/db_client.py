import os
import time
import json
import requests
from urllib.parse import urljoin


class NotionClient:
    def __init__(self) -> None:
        self.notion_secret = os.environ.get(
            "NOTION_SECRET", "secret_qjSxb7ZfRAnkt34usnWzlmeEOSCtUpJL3iMipRtSToi")
        self.notion_version = "2022-06-28"
        self.database_id = os.environ.get(
            "NOTION_DATABASE_ID", "d3d26c3147ed42d6861f0c05a317f443")

        self.headers = self.getHeaders()
        self.api_endpoint = "https://api.notion.com/v1/"
        self.pages_endpoint = urljoin(self.api_endpoint, "pages/")
        self.db_endpoint = urljoin(self.api_endpoint, f"databases/{self.database_id}/")
        self.query_endpoint = urljoin(self.db_endpoint, "query/")        
        self.retry_depth = 5

    def getHeaders(self) -> dict:
        return {
            "Authorization": f"Bearer {self.notion_secret}",
            "Notion-version": self.notion_version,
            "Content-Type": "application/json",
        }

    def resourceExists(self, url) -> str:
        data = {
            "filter": {
                "property": "URL",
                "url": {
                    "equals": url
                }
            }
        }

        resp = requests.post(
            self.query_endpoint,
            data=json.dumps(data),
            headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()
            if len(data['results']) == 1:
                return data["results"][0]["id"]
        return False

    def _title(self, title):
        if title is None:
            return None
        return {"title": [{"text": {"content": title}}]}

    def _source(self, source):
        if source is None:
            return None
        return {"select": {"name": source}}

    def _tags(self, tags):
        if tags is None or len(tags) == 0:
            return {"multi_select": []}
        return {"multi_select": [{"name": tag.replace(",", "")} for tag in tags]}
    
    def _authors(self, authors):
        if authors is None or len(authors) == 0:
            return {"multi_select": []}
        return {"multi_select": [{"name": author.replace(",", "")} for author in authors]}

    def _url(self, url):
        if url is None:
            return None
        return {"url": url}

    def _publishedOn(self, publishedOn):
        if publishedOn is None:
            return {"date": None}
        return { "date": {"start": publishedOn}}

    def addResource(self, **kwargs):
        data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Title": self._title(kwargs.get("title")),
                "Source": self._source(kwargs.get("source")),
                "Tags": self._tags(kwargs.get("tags")),
                "Authors": self._authors(kwargs.get("authors")),
                "URL": self._url(kwargs.get("url")),
                "Published On": self._publishedOn(kwargs.get("publishedOn"))
            }
        }

        resp = requests.post(self.pages_endpoint, data=json.dumps(data), headers=self.headers)
        if resp.status_code == 429:

            retry_depth = kwargs.get("retry_depth", 0)
            if retry_depth > self.retry_depth:
                print("Retry Depth", resp.json())
                return False
            time.sleep(1)
            kwargs["retry_depth"] = retry_depth + 1
            return self.addResource(self, **kwargs)
        elif resp.status_code == 200:
            return True
        print("Resp", resp.json())
        return False

    def updateResource(self, **kwargs):
        data = {
            "properties": {
                "Title": self._title(kwargs.get("title")),
                "Source": self._source(kwargs.get("source")),
                "Tags": self._tags(kwargs.get("tags")),
                "Authors": self._authors(kwargs.get("authors")),
                "URL": self._url(kwargs.get("url")),
                "Published On": self._publishedOn(kwargs.get("publishedOn"))
            }
        }
        page_id = kwargs.get("page_id", None)
        if page_id is None:
            return False

        page_endpoint = urljoin(self.pages_endpoint, page_id)
        resp = requests.patch(page_endpoint, data=json.dumps(data), headers=self.headers)
        if resp.status_code == 200:
            return True
        elif resp.status_code == 404:
            return False
        
        retry_depth = kwargs.get("retry_depth", 0)
        if retry_depth > self.retry_depth:
            return False
        time.sleep(1)
        kwargs["retry_depth"] = retry_depth + 1
        return self.updateResource(**kwargs)

    def deleteResource(self, **kwargs):
        data = {"archived": True}
        page_id = kwargs.get("page_id", None)
        if page_id is None:
            return False

        page_endpoint = urljoin(self.pages_endpoint, page_id)
        resp = requests.patch(page_endpoint, data=json.dumps(data), headers=self.headers)
        
        if resp.status_code == 200:
            return True
        elif resp.status_code == 404:
            return False

        retry_depth = kwargs.get("retry_depth", 0)
        if retry_depth > self.retry_depth:
            return False
        time.sleep(1)
        kwargs["retry_depth"] = retry_depth + 1
        return self.deleteResource(**kwargs)
    
    def sourceExists(self, source):
        data = {
            "filter": {
                "property": "Source",
                "select": {
                    "equals": source 
                }
            }
        }

        resp = requests.post(self.query_endpoint, data=json.dumps(data), headers=self.headers)
        if resp.status_code == 200:
            data = resp.json()
            if len(data['results']) > 0:
                return True
        return False