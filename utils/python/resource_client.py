import os
from datetime import datetime
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

        self.db.handleSource(self.title, self.url, self.icon)
        self.source_id = self.db.getSourceId(self.title)
        self.dateFormat = dateFormat
        self.refetch = int(os.environ.get("REFETCH", 0)) == 1

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

    def formatAuthors(self, authors: str) -> str:
        if authors is None:
            return authors

        return authors.strip()

    def formatTags(self, tags: str) -> str:
        if tags is None:
            return ",".join([])

        tags = tags.strip().split(',')
        return ",".join(list(map(lambda x: x.strip(), tags)))