import { Logger, createLogger, format, transports } from "winston";
import { DBClient } from "utils/js/db_client";
import date from "date-and-time";

class ResourceClient {
  title: string;
  url: string;
  icon: string;
  dateFormat: string;
  logger: Logger;
  db: DBClient;
  source_id: string;
  refetch: boolean;

  constructor(title: string, url: string, icon: string, dateFormat: string) {
    this.logger = createLogger({
      level: "info",
      format: format.combine(
        format.timestamp({ format: "YYYY-MM-DD HH:mm:ss" }),
        format.printf(({ level, message, label, timestamp }) => {
          return `[${level}]:[${timestamp}]:[${title}] ${message}`;
        })
      ),
      transports: [new transports.File({ filename: "resource_scrapper.log", level: "info" })],
    });

    this.db = new DBClient("database.db", this.logger);

    this.title = title;
    this.url = url;
    this.icon = icon;
    this.dateFormat = dateFormat;

    this.db.handleSource(this.title, this.url, this.icon);

    this.source_id = this.db.getSourceId(title);
    this.refetch = process.env.REFETCH == "1";
  }

  formatTitle(title: string) {
    return title.trim();
  }

  formatURL(url: string) {
    return url.trim();
  }

  formatPublishedOn(date_str?: string) {
    if (!date_str) return date_str;

    date_str = date_str.trim();
    let publishedOn = date_str;
    try {
      publishedOn = date.parse(date_str, this.dateFormat).toUTCString();
    } catch (err) {
      console.log("Invalid dateformat");
    }
    return publishedOn;
  }

  formatAuthors(authors?: string | Array<string>) {
    if (!authors) return authors;
    if (typeof authors === "string") return authors.trim();
    return authors.map((author) => author.trim()).join(",");
  }

  formatTags(tags?: string | Array<string>) {
    if (!tags) return tags;
    if (typeof tags === "string") return tags.trim();
    return tags.map((tag) => tag.trim()).join(",");
  }
}

export { ResourceClient };