import 'package:aibook/widgets/bookmarked_resources_list.dart';
import 'package:flutter/material.dart';

class BookmarkedResourcesScreen extends StatelessWidget {
  const BookmarkedResourcesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF3A3C41),
        title: const Text("Bookmarked Resources"),
      ),
      body: BookmarkedResourcesList(),
    );
  }
}
