import 'dart:convert';

import 'package:aibook/widgets/resource_item.dart';
import 'package:aibook/utils/resource.dart';
import 'package:flutter/material.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:http/http.dart' as http;
import 'package:shimmer/shimmer.dart';

class AllResourcesList extends StatefulWidget {
  final ScrollController? controller;
  const AllResourcesList({
    Key? key,
    this.controller,
  }) : super(key: key);

  @override
  State<AllResourcesList> createState() => _AllResourcesListState();
}

class _AllResourcesListState extends State<AllResourcesList> {
  final PagingController<int, Resource> _pagingController =
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
    return PagedListView<int, Resource>(
      scrollController: widget.controller,
      pagingController: _pagingController,
      builderDelegate: PagedChildBuilderDelegate<Resource>(
        itemBuilder: (context, resource, index) => ResourceItem(
          resource: resource,
          showSource: true,
        ),
        firstPageProgressIndicatorBuilder: (context) {
          return Shimmer.fromColors(
            baseColor: Colors.grey[300]!,
            highlightColor: Colors.grey[100]!,
            child: ListView.builder(
              itemCount: 30,
              itemBuilder: (context, idx) => const Card(
                child: ListTile(),
              ),
            ),
          );
        },
        newPageProgressIndicatorBuilder: (context) {
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
      ),
    );
  }

  Future<void> _fetchPage(int pageKey) async {
    String endpoint =
        "https://raw.githubusercontent.com/sleepingsaint/AI-Book/db/allResources/$pageKey.json";
    try {
      final response = await http.get(Uri.parse(endpoint));
      if (response.statusCode == 200) {
        List<Resource> resources = [];
        Map<String, dynamic> data = jsonDecode(response.body);
        for (int i = 0; i < data['data'].length; i++) {
          resources.add(Resource.fromJSON(data["data"][i]));
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
