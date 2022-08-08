import logging
import re
import sys
import sqlite3
from sqlite3 import Error as SQLError

class DBClient:
    def __init__(self, db_path, logger: logging.Logger) -> None:
        # connecting to database and creating required tables
        self.conn = self.__getDBConn(db_path)
        self.logger = logger
        if self.conn is None:
            logger.error("[DATABASE] Cannot able to connect to database")
            return sys.exit("Cannot able to connect to database")
        if not self.__ensureTables():
            logger.error("[DATABASE] Cannot able to create tables")
            return sys.exit("Cannot able to create tables")
        
    def __getDBConn(self, db_path):
        conn = None
        try:
            conn = sqlite3.connect(db_path)
        except SQLError as e:
            self.logger.error(e)
            print(e)
        return conn

    def __ensureTables(self):
        sources_table_sql = """CREATE TABLE IF NOT EXISTS sources (
                id INTEGER PRIMARY KEY,
                source_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                icon TEXT NOT NULL
            );"""
        resources_table_sql = """CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                resource_id TEXT NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                authors TEXT,
                tags TEXT,
                publishedOn TEXT,
                source_id INTEGER NOT NULL,
                FOREIGN KEY (source_id) REFERENCES sources (id) ON DELETE CASCADE
            );"""
        
        if not self.__handleDBTransaction(sources_table_sql, None):
            return False
        
        if not self.__handleDBTransaction(resources_table_sql, None):
            return False
        
        return True
        
    
    def __formatId(self, id):
        return re.sub("[^0-9a-z]", "", id.lower())
    
    # handle database transactions like insert, update, delete
    def __handleDBTransaction(self, sql, params):
        if params is None:
            try:
                c = self.conn.cursor()
                c.execute(sql)
            except SQLError as e:
                print(e)
                return False
            return True

        try:
            c = self.conn.cursor()
            c.execute(sql, params)
            self.conn.commit()
        except SQLError as e:
            print(e)
            return False
        return True

    # handle database queries like SELECT
    def __handleDBQuery(self, sql, params):
        try:
            c = self.conn.cursor()
            c.execute(sql, params)
            rows = c.fetchall()
        except SQLError as e:
            print(e)
            return None
        return rows

    # source utils functions
    def __checkSource(self, title):
        source_id = self.__formatId(title)
        sql = """SELECT * FROM sources where source_id = ?"""
        res = self.__handleDBQuery(sql, (source_id,))
        if res is None or len(res) == 0:
            return False
        return True
    
    def __addSource(self, title, url, icon):
        sql = """INSERT INTO sources (source_id, title, url, icon) VALUES (?, ?, ?, ?)"""
        if self.__handleDBTransaction(sql, (self.__formatId(title), title, url, icon)):
            self.logger.info(f"[SOURCE]:[ADD] {title}")
            return True

        self.logger.error(f"[SOURCE]:[ADD] {title}")
        return False

    def __updateSource(self, title, url=None, icon=None):
        if url is None and icon is None:
            return True

        if not self.__checkSource(title):
            return False

        source_id = self.__formatId(title)
        if url is not None:
            sql = """UPDATE sources SET icon = ? WHERE source_id = ?"""
            if not self.__handleDBTransaction(sql, (icon, source_id)):
                self.logger.error(f"[SOURCE]:[UPDATE] {title}")
                return False
        
        if icon is not None:
            sql = """UPDATE sources SET url = ? WHERE source_id = ?"""
            if not self.__handleDBTransaction(sql, (url, source_id)):
                self.logger.error(f"[SOURCE]:[UPDATE] {title}")
                return False

        self.logger.info(f"[SOURCE]:[UPDATE] {title}")
        return True
    
    def __deleteSource(self, title):
        source_id = self.__formatId(title)
        if not self.__checkSource(title):
            return True
        sql = """DELETE FROM sources WHERE source_id = ?"""
        if not self.__handleDBTransaction(sql, (source_id,)):
            self.logger.error(f"[SOURCE]:[DELETE] {title}")
            return False

        self.logger.info(f"[SOURCE]:[DELETE] {title}")
        return True

    # resource util functions
    def __checkResource(self, title):
        resource_id = self.__formatId(title)
        sql = """SELECT * FROM resources WHERE resource_id = ?"""
        res = self.__handleDBQuery(sql, (resource_id,))
        if res is None or len(res) == 0:
            return False
        return True
    
    def __addResource(self, source_id, title, url, authors, tags, publishedOn):
        sql = """INSERT INTO resources (resource_id, title, url, authors, tags, publishedOn, source_id) VALUES (?, ?, ?, ?, ?, ?, ?)"""
        resource_id = self.__formatId(title)
        if not self.__handleDBTransaction(sql, (resource_id, title, url, authors, tags, publishedOn, source_id)):
            self.logger.error(f"[RESOURCE]:[ADD] {title}")
            return False

        self.logger.info(f"[RESOURCE]:[ADD] {title}")
        return True

    def __updateResource(self, source_id, title, url=None, authors=None, tags=None, publishedOn=None):
        if not self.__checkResource(title):
            return False

        resource_id = self.__formatId(title)
        if url is not None:
            sql = """UPDATE resources SET url = ? WHERE resource_id = ?"""
            if not self.__handleDBTransaction(sql, (url, resource_id)):
                self.logger.error(f"[RESOURCE]:[UPDATE] {title}")
                return False

        if authors is not None:
            sql = """UPDATE resources SET authors = ? WHERE resource_id = ?"""
            if not self.__handleDBTransaction(sql, (authors, resource_id)):
                self.logger.error(f"[RESOURCE]:[UPDATE] {title}")
                return False

        if tags is not None:
            sql = """UPDATE resources SET tags = ? WHERE resource_id = ?"""
            if not self.__handleDBTransaction(sql, (tags, resource_id)):
                self.logger.error(f"[RESOURCE]:[UPDATE] {title}")
                return False

        if publishedOn is not None:
            sql = """UPDATE resources SET publishedOn = ? WHERE resource_id = ?"""
            if not self.__handleDBTransaction(sql, (publishedOn, resource_id)):
                self.logger.error(f"[RESOURCE]:[UPDATE] {title}")
                return False
        
        self.logger.info(f"[RESOURCE]:[UPDATE] {title}")
        return True

    def __deleteResource(self, title):
        if not self.__checkResource(title):
            return True
        sql = """DELETE FROM resources WHERE resource_id = ?"""
        resource_id = self.__formatId(title)
        if not self.__handleDBTransaction(sql, (resource_id,)):
            self.logger.error(f"[RESOURCE]:[DELETE] {title}")
            return False

        self.logger.info(f"[RESOURCE]:[DELETE] {title}")
        return True

    def handleSource(self, title, url, icon, delete=False):
        if title is None:
            return False

        if delete:
            return self.__deleteSource(title)
        if not self.__checkSource(title):
            return self.__addSource(title, url, icon)
        return self.__updateSource(title, url, icon)
        
    def handleResource(self, source_id, title, url, authors, tags, publishedOn, delete=False):
        if title is None:
            return False

        if delete:
            return self.__deleteResource(title)        
        if not self.__checkResource(title):
            return self.__addResource(source_id, title, url, authors, tags, publishedOn)
        return self.__updateResource(source_id, title, url, authors, tags, publishedOn)
    
    def getSourceId(self, title):
        resource_id = self.__formatId(title)
        sql = """SELECT * FROM sources WHERE source_id = ?"""
        res = self.__handleDBQuery(sql, (resource_id,))
        if res is None or len(res) == 0:
            return None
        return res[0][0]
    
    def resourceExists(self, title):
        return self.__checkResource(title)