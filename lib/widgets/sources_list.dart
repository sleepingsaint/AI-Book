import 'dart:convert';

import 'package:aibook/widgets/source_item.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:http/http.dart' as http;
import 'package:shimmer/shimmer.dart';

class SourcesList extends StatefulWidget {
  const SourcesList({Key? key}) : super(key: key);

  @override
  State<SourcesList> createState() => _SourcesListState();
}

class _SourcesListState extends State<SourcesList> {
  final PagingController<int, Source> _pagingController =
      PagingController(firstPageKey: 0);

  @override
  void initState() {
    _pagingController.addPageRequestListener((pageKey) {
      _fetchPage(pageKey);
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: PagedGridView<int, Source>(
        pagingController: _pagingController,
        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: 2,
          crossAxisSpacing: 4.0,
          mainAxisSpacing: 4.0,
        ),
        builderDelegate: PagedChildBuilderDelegate(
          itemBuilder: (context, source, idx) => SourceItem(
            source: source,
          ),
          firstPageProgressIndicatorBuilder: (context) {
            return Shimmer.fromColors(
              baseColor: Colors.grey[300]!,
              highlightColor: Colors.grey[100]!,
              child: GridView.builder(
                itemCount: 30,
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                ),
                itemBuilder: (context, idx) => const Card(),
              ),
            );
          },
          newPageProgressIndicatorBuilder: (context) {
            return Shimmer.fromColors(
              baseColor: Colors.grey[300]!,
              highlightColor: Colors.grey[100]!,
              child: GridView.builder(
                itemCount: 10,
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                ),
                itemBuilder: (context, idx) => const Card(),
              ),
            );
          },
        ),
      ),
    );
  }

  Future<void> _fetchPage(int pageKey) async {
    try {
      final response = await http.get(Uri.parse(
          "https://raw.githubusercontent.com/sleepingsaint/AI-Book/db/sources/$pageKey.json"));
      if (response.statusCode == 200) {
        List<Source> resources = [];
        Map<String, dynamic> data = jsonDecode(response.body);
        for (int i = 0; i < data['data'].length; i++) {
          resources.add(Source.fromJSON(data["data"][i]));
        }

        if (!data["hasNextPage"]) {
          _pagingController.appendLastPage(resources);
        } else {
          _pagingController.appendPage(resources, pageKey + 1);
        }
      }
    } catch (error) {
      _pagingController.error = error;
    }
  }

  @override
  void dispose() {
    _pagingController.dispose();
    super.dispose();
  }
}
