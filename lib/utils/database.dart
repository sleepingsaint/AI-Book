import 'package:aibook/utils/resource.dart';
import 'package:flutter/foundation.dart';
import 'package:hive_flutter/hive_flutter.dart';

class DatabaseClient {
  static late Box<Resource> box;
  static const String boxName = "bookmarked_resources";

  static final DatabaseClient _instance = DatabaseClient._internal();

  factory DatabaseClient() {
    return _instance;
  }

  DatabaseClient._internal();

  static Future<void> initDB() async {
    await Hive.initFlutter();
    Hive.registerAdapter(ResourceAdapter());
    box = await Hive.openBox(boxName);
  }

  ValueListenable<Box<Resource>> getAllBookmarkedResourcesListenable() {
    return box.listenable();
  }

  ValueListenable<Box<Resource>> getListenable(int key) {
    return box.listenable(keys: [key]);
  }

  Future<List<Resource>> getResources() async {
    return [];
  }

  Future<bool> addResource(Resource resource) async {
    return true;
  }

  Future<bool> removeResource(Resource resource) async {
    return true;
  }

  Future<bool> checkResource(Resource resource) async {
    return box.get(resource.id) != null;
  }
}
