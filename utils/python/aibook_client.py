from datetime import datetime
from typing import List, Union
from linkpreview import Link, LinkGrabber, LinkPreview 
from utils.python.resource_client import ResourceClient

class FakeLinkPreview:
    def __init__(self) -> None:
        self.description = None
        self.image = None

class AIBookClient(ResourceClient):
    def __init__(self, title: str, url: str, dateFormat: str) -> None:
        super().__init__(title, url)
        self.url = url
        self.dateFormat = dateFormat

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
        return ", ".join(list(map(lambda x: x.strip(), authors)))
        
    def formatTags(self, tags: Union[str, List[str], None] = None) -> str:
        if tags is None:
            return tags 
        
        if type(tags) is str:
            tags = tags.strip().split(',')
        return ", ".join(list(map(lambda x: x.strip(), tags)))

    def handleResource(self, title, url, authors, tags, publishedOn, description, thumbnail):
        if not self.db.resourceExists(url): 
            result = self.db.handleResource(self.source_id, title, url, authors, tags, publishedOn, description, thumbnail)
            if not result:
                print(f"Resource cannot be created : {title}")
                return False
            return True
        
        elif self.refetch:
            if not self.db.handleResource(self.source_id, title, url, authors, tags, publishedOn, description, thumbnail):
                print(f"Resource cannot be updated : {title}")
            return True

        return False
    
    def getPreview(self, url):
        try:
            grabber = LinkGrabber(
                initial_timeout=20, maxsize=1e+9, receive_timeout=100, chunk_size=1024,
            )
            content, url = grabber.get_content(url)
            link = Link(url, content)
            preview = LinkPreview(link)
            return preview
        except:
            return FakeLinkPreview()