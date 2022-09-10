import os
from datetime import datetime
from typing import List, Union
from utils.python.db_client import DBClient
import logging

class ResourceClient:
    def __init__(self, title: str, url: str, icon: str, dateFormat: str) -> None:
        logging_format=f"[%(levelname)s]:[%(asctime)s]:[{title}] %(message)s"
        logging.basicConfig(filename="resource_scrapper.log", format=logging_format)
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)

        self.db = DBClient("database.db", self.logger)
        self.title = title
        self.url = url
        self.icon = icon

        # flag to refetch the entire posts or just check for new posts
        # if source is not added yet or manually enter
        self.refetch = int(os.environ.get("REFETCH", 0)) == 1
        self.refetch = self.refetch or not self.db.sourceExists(title)

        self.db.handleSource(self.title, self.url, self.icon)
        self.dateFormat = dateFormat
        self.source_id = self.db.getSourceId(self.title)

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
        return ",".join(list(map(lambda x: x.strip(), authors)))
        
    def formatTags(self, tags: Union[str, List[str], None] = None) -> str:
        if tags is None:
            return ",".join([])
        
        if type(tags) is str:
            tags = tags.strip().split(',')
        return ",".join(list(map(lambda x: x.strip(), tags)))
