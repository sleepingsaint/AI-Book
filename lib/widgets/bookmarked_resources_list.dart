import 'package:aibook/utils/database.dart';
import 'package:aibook/utils/resource.dart';
import 'package:aibook/widgets/resource_item.dart';
import 'package:flutter/material.dart';
import 'package:shimmer/shimmer.dart';

class BookmarkedResourcesList extends StatelessWidget {
  BookmarkedResourcesList({Key? key}) : super(key: key);
  final DatabaseHelper helper = DatabaseHelper();
  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Resource>>(
      future: helper.getResources(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return ListView.builder(
            itemCount: snapshot.data!.length,
            itemBuilder: (context, index) => ResourceItem(
              resource: snapshot.data![index],
            ),
          );
        }
        if (snapshot.hasError) {
          return const Center(
            child: Text("Oops! Something went wrong"),
          );
        }
        return Shimmer.fromColors(
          baseColor: Colors.grey[300]!,
          highlightColor: Colors.grey[100]!,
          child: ListView.builder(
            itemCount: 10,
            itemBuilder: (context, idx) => const Card(
              child: ListTile(),
            ),
          ),
        );
      },
    );
  }
}
