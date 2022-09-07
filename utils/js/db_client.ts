import { Database } from "sqlite3";
import { Logger } from "winston";

class DBClient {
  logger: Logger;
  db: Database;

  constructor(db_path: string, logger: Logger) {
    this.logger = logger;
    this.db = new Database(db_path, (err) => {
      if (err) {
        logger.error("[DATABASE] Cannot able to connect to database");
        throw "Cannot able to connect to database";
      }
    });

    if (!this.__ensureTables()) {
      logger.error("[DATABASE] Cannot able to create tables");
      throw "Cannot able to create tables";
    }
  }

  __ensureTables() {
    const sources_table_sql = `
        CREATE TABLE IF NOT EXISTS sources (
            id INTEGER PRIMARY KEY,
            source_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            icon TEXT NOT NULL
        );`;
    const resources_table_sql = `
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY,
            resource_id TEXT NOT NULL,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            authors TEXT,
            tags TEXT,
            publishedOn TEXT,
            source_id INTEGER NOT NULL,
            FOREIGN KEY (source_id) REFERENCES sources (id) ON DELETE CASCADE
        );`;

    if (!this.__handleDBTransaction(sources_table_sql)) {
      return false;
    }

    if (!this.__handleDBTransaction(resources_table_sql)) {
      return false;
    }

    return true;
  }

  __handleDBTransaction(sql: string, params?: Object) {
    if (params) {
      this.db.run(sql, params, (err) => {
        if (err) return false;
        return true;
      });
    }

    this.db.run(sql, (err) => {
      if (err) return false;
      return true;
    });
    return true;
  }

  __handleDBQuery(sql: string, params?: Object) {
    let res: any[];
    this.db.all(sql, params, (err, rows) => {
      if (err) return null;
      res = rows;
    });
    return res;
  }

  __formatId(id: string) {
    return id.toLowerCase().replace(new RegExp("[^0-9a-z]"), "");
  }

  __checkSource(title: string) {
    const source_id = this.__formatId(title);
    const sql = "SELECT * FROM source where source_id = ?";
    const res = this.__handleDBQuery(sql, [source_id]);
    if (res == null || res.length == 0) {
      return false;
    }
    return true;
  }

  __addSource(title: string, url: string, icon: string) {
    const sql = "INSERT INTO sources (source_id, title, url, icon) VALUES (?, ?, ?, ?)";
    const source_id = this.__formatId(title);
    if (!this.__handleDBTransaction(sql, [source_id, title, url, icon])) {
      this.logger.info(`[SOURCE]:[ADD] ${title}`);
      return true;
    }

    this.logger.error(`[SOURCE]:[ADD] ${title}`);
    return false;
  }

  __updateSource(title: string, url?: string, icon?: string) {
    if (!url || !icon) return true;
    if (!this.__checkSource(title)) return false;
    const source_id = this.__formatId(title);

    if (url) {
      const sql = "UPDATE sources SET url = ? WHERE source_id = ?";
      if (!this.__handleDBTransaction(sql, [url, source_id])) {
        this.logger.error(`[SOURCE]:[UPDATE] ${title}`);
        return false;
      }
    }

    if (icon) {
      const sql = "UPDATE sources SET icon = ? WHERE source_id = ?";
      if (!this.__handleDBTransaction(sql, [icon, source_id])) {
        this.logger.error(`[SOURCE]:[UPDATE] ${title}`);
        return false;
      }
    }

    this.logger.info(`[SOURCE]:[UPDATE] ${title}`);
    return true;
  }

  __deleteSource(title: string) {
    const source_id = this.__formatId(title);
    if (!this.__checkSource(title)) {
      return true;
    }

    const sql = "DELETE FROM sources WHERE source_id = ?";
    if (!this.__handleDBTransaction(sql, [source_id])) {
      this.logger.error(`[SOURCE]:[DELETE] ${title}`);
      return false;
    }

    this.logger.info(`[SOURCE]:[DELETE] ${title}`);
    return true;
  }

  __checkResource(title: string) {
    const resource_id = this.__formatId(title);
    const sql = "SELECT * FROM resources WHERE resource_id = ?";
    const res = this.__handleDBQuery(sql, [resource_id]);
    if (!res || res.length == 0) {
      return false;
    }
    return true;
  }

  __addResource(source_id: string, title: string, url: string, authors: string, tags: string, publishedOn: string) {
    const sql =
      "INSERT INTO resources (resource_id, title, url, authors, tags, publishedOn, source_id) VALUES (?, ?, ?, ?, ?, ?, ?)";
    const resource_id = this.__formatId(title);
    if (!this.__handleDBTransaction(sql, [resource_id, title, url, authors, tags, publishedOn, source_id])) {
      this.logger.error(`[RESOURCE]:[ADD] ${title}`);
      return false;
    }
    this.logger.info(`[RESOURCE]:[ADD] ${title}`);
    return true;
  }

  __updateResource(
    source_id: string,
    title: string,
    url?: string,
    authors?: string,
    tags?: string,
    publishedOn?: string
  ) {
    if (!this.__checkResource(title)) return false;
    const resource_id = this.__formatId(title);
    if (!url) {
      const sql = "UPDATE resources SET url = ? WHERE resource_id = ?";
      if (!this.__handleDBTransaction(sql, [url, resource_id])) {
        this.logger.error(`[RESOURCE]:[UPDATE] ${title}`);
        return false;
      }
    }
    if (!authors) {
      const sql = "UPDATE resources SET authors = ? WHERE resource_id = ?";
      if (!this.__handleDBTransaction(sql, [authors, resource_id])) {
        this.logger.error(`[RESOURCE]:[UPDATE] ${title}`);
        return false;
      }
    }
    if (!tags) {
      const sql = "UPDATE resources SET tags = ? WHERE resource_id = ?";
      if (!this.__handleDBTransaction(sql, [tags, resource_id])) {
        this.logger.error(`[RESOURCE]:[UPDATE] ${title}`);
        return false;
      }
    }
    if (!publishedOn) {
      const sql = "UPDATE resources SET publishedOn = ? WHERE resource_id = ?";
      if (!this.__handleDBTransaction(sql, [publishedOn, resource_id])) {
        this.logger.error(`[RESOURCE]:[UPDATE] ${title}`);
        return false;
      }
    }

    this.logger.info(`[RESOURCE]:[UPDATE] ${title}`);
    return true;
  }

  __deleteResource(title: string) {
    if (!this.__checkResource(title)) return true;
    const sql = "DELETE FROM resources WHERE resource_id = ?";
    const resource_id = this.__formatId(title);
    if (!this.__handleDBTransaction(sql, [resource_id])) {
      this.logger.error(`[RESOURCE]:[DELETE] ${title}`);
      return false;
    }

    this.logger.info(`[RESOURCE]:[DELETE] ${title}`);
    return true;
  }

  handleSource(title: string, url: string, icon: string, _delete: boolean = false) {
    if (!title || !url) return false;

    if (_delete) return this.__deleteSource(title);
    if (!this.__checkSource(title)) return this.__addSource(title, url, icon);
    return this.__updateSource(title, url, icon);
  }

  handleResource(
    source_id: string,
    title: string,
    url: string,
    authors: string,
    tags: string,
    publishedOn: string,
    _delete = false
  ) {
    if (_delete) return this.__deleteResource(title);
    if (!this.__checkResource(title)) return this.__addResource(source_id, title, url, authors, tags, publishedOn);
    return this.__updateResource(source_id, title, url, authors, tags, publishedOn);
  }

  getSourceId(title: string) {
    const source_id = this.__formatId(title);
    const sql = "SELECT * FROM sources WHERE source_id = ?";
    const res = this.__handleDBQuery(sql, [source_id]);
    if (!res || res.length == 0) return null;
    return res[0][0];
  }

  resourceExists(title: string) {
    return this.__checkResource(title);
  }
}

export { DBClient };