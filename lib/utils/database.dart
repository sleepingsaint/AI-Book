import 'package:aibook/utils/resource.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static late Database db;
  static const String databaseName = "aibook.db";
  static const String table = "resources";

  static final DatabaseHelper _instance = DatabaseHelper._internal();

  factory DatabaseHelper() {
    return _instance;
  }

  DatabaseHelper._internal();

  static Future<void> removeDB() async {
    String databasesPath = await getDatabasesPath();
    String path = join(databasesPath, databaseName);
    await deleteDatabase(path);
  }

  static Future<void> initDB() async {
    String databasesPath = await getDatabasesPath();
    String path = join(databasesPath, databaseName);

    db = await openDatabase(
      path,
      version: 1,
      onCreate: (Database db, int version) async {
        await db.execute(
          """
             CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                authors TEXT,
                tags TEXT,
                publishedOn TEXT,
                description TEXT,
                thumbnail TEXT,
                sourceId INTEGER NOT NULL,
                source TEXT NOT NULL
            );
          """,
        );
      },
    );
  }

  Future<List<Resource>> getResources() async {
    try {
      List<Map<String, dynamic>> data = await db.query(table);
      List<Resource> res = [];
      for (int i = 0; i < data.length; i++) {
        res.add(Resource.fromJSON(data[i]));
      }
      return res;
    } catch (er) {
      return [];
    }
  }

  Future<bool> addResource(Resource resource) async {
    try {
      Map<String, dynamic> row = {
        "title": resource.title,
        "url": resource.url,
        "authors": resource.authors,
        "tags": resource.tags,
        "publishedOn": resource.publishedOn,
        "description": resource.description,
        "thumbnail": resource.thumbnail,
        "sourceId": resource.sourceId,
        "source": resource.source,
      };
      await db.insert(table, row);
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> removeResource(Resource resource) async {
    try {
      await db.delete(table, where: "url = ?", whereArgs: [resource.url]);
      return true;
    } catch (e) {
      return false;
    }
  }

  Future<bool> checkResource(Resource resource) async {
    List<Map> result = await db.query(
      table,
      where: "url = ?",
      whereArgs: [
        resource.url,
      ],
    );
    return result.isNotEmpty;
  }
}
