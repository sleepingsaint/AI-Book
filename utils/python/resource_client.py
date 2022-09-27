import os
from datetime import datetime
from typing import List, Union
from utils.python.db_client import NotionClient
from utils.python.social_client import SocialClient

class ResourceClient(SocialClient):
    def __init__(self, source: str, dateFormat: str) -> None:
        super().__init__()

        self.db = NotionClient()
        self.source = source 
        self.dateFormat = dateFormat

        # flag to refetch the entire posts or just check for new posts
        # if source is not added yet or manually enter
        self.refetch = int(os.environ.get("REFETCH", 0)) == 1
        self.new_source = not self.db.sourceExists(source)
        self.refetch = self.refetch or self.new_source
        self.delete = int(os.environ.get("DELETE", 0)) == 1
    
    def formatTitle(self, title: str) -> str:
        return title.strip()

    def formatURL(self, url: str) -> str:
        return url.strip()

    def formatPublishedOn(self, date: str) -> str:
        if date is None or self.dateFormat is None:
            return date

        date = date.strip()
        publishedOn = date
        try:
            _datetime = datetime.strptime(date, self.dateFormat)
            publishedOn = _datetime.isoformat()
        except:
            print("Invalid date format")

        return publishedOn

    def formatAuthors(self, authors: Union[str, List[str], None]):
        if authors is None:
            return authors
        
        if type(authors) is str:
            return authors.strip()
        return authors
        
    def formatTags(self, tags: Union[str, List[str], None] = None) -> str:
        if tags is None:
            return tags
        
        if type(tags) is str:
            tags = tags.strip().split(',')
        return tags