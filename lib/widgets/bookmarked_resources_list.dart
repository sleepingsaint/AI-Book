import 'package:aibook/utils/database.dart';
import 'package:aibook/utils/resource.dart';
import 'package:aibook/widgets/resource_item.dart';
import 'package:flutter/material.dart';
import 'package:hive/hive.dart';

class BookmarkedResourcesList extends StatelessWidget {
  BookmarkedResourcesList({Key? key}) : super(key: key);
  final DatabaseClient client = DatabaseClient();
  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder<Box<Resource>>(
      valueListenable: client.getAllBookmarkedResourcesListenable(),
      builder: (context, box, widget) {
        Map<dynamic, Resource> raw = box.toMap();
        List<Resource> resources = raw.values.toList();
        return ListView.builder(
          itemCount: resources.length,
          itemBuilder: (context, index) {
            return ResourceItem(resource: resources[index]);
          },
        );
      },
    );
  }
}
