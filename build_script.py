import os
import sys
import json
import shutil
import sqlite3
from sqlite3 import Error as SQLError

class DataBuilder:
    def __init__(self, db_path="database.db") -> None:
        self.conn = self.__getDBConn(db_path)
        if self.conn is None:
            return sys.exit("Connecting to database failed")
        self.source_page_size = 50
        self.resource_page_size = 30

    def __getDBConn(self, db_path):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except SQLError as e:
            self.logger.error(e)
            print(e)
        return conn
    
    def __handleDBQuery(self, sql, params):
        try:
            c = self.conn.cursor()
            c.execute(sql, params)
            rows = c.fetchall()
        except SQLError as e:
            print(e)
            return None
        return rows

    def __ensureDir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def __removeDirs(self, path):
        if os.path.exists(path):
            shutil.rmtree(path)

    def getSources(self):
        sql = "SELECT * FROM sources"
        return self.__handleDBQuery(sql, ())

    def getNumResources(self, source_id):
        sql = "SELECT COUNT(*) FROM resources where source_id = ?"
        res = self.__handleDBQuery(sql, (source_id,))
        if not res or len(res) == 0:
            return 0
        return res[0][0]

    def buildSources(self, data):
        def __formatSource(data):
            formatted_sources = []
            for source in data:
                num_resources = self.getNumResources(source[0])
                num_resource_pages = (num_resources // self.resource_page_size) + (num_resources % self.resource_page_size > 0)
                formatted_sources.append({
                    "source_db_id": source[0],
                    "source_id": source[1],
                    "title": source[2],
                    "url": source[3],
                    "icon": source[4],
                    "num_resources": num_resources,
                    "num_resource_pages": num_resource_pages
                })
            return formatted_sources

        self.__removeDirs("sources")
        self.__ensureDir("sources")

        idx, page_id = 0, 0
        while idx < len(data):
            with open(f"sources/{page_id}.json", "w+") as f:
                json.dump(__formatSource(data[idx:min(idx+self.source_page_size, len(data))]), f, indent=4)
            idx = min(idx+self.source_page_size, len(data))
            page_id += 1

    def buildResources(self, source_id, data):
        def __formatResources(data):
            formattedResources = []
            for resource in data:
                formattedResources.append({
                    "resource_db_id": resource[0],
                    "resource_id": resource[1],
                    "title": resource[2],
                    "url": resource[3],
                    "authors": resource[4],
                    "tags": resource[5],
                    "publishedOn": resource[6]
                })
            return formattedResources

        self.__removeDirs(f"resources/{source_id}")
        self.__ensureDir(f"resources/{source_id}")
        
        idx, page_id = 0, 0
        while idx < len(data):
            with open(f"resources/{source_id}/{page_id}.json", "w+") as f:
                json.dump(__formatResources(data[idx:min(idx+self.resource_page_size, len(data))]), f, indent=4)
            idx = min(idx + self.resource_page_size, len(data))
            page_id += 1

    def getResources(self, source_id):
        sql = "SELECT * FROM resources WHERE source_id = ? ORDER BY publishedOn DESC"
        return self.__handleDBQuery(sql, (source_id,))

    def build(self):
        sources = self.getSources()
        self.buildSources(sources)
        for source in sources:
            resources = self.getResources(source[0])
            self.buildResources(source[1], resources)
        
data_builder = DataBuilder()
data_builder.build()