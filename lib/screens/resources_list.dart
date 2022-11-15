import 'dart:convert';

import 'package:aibook/screens/resource_item.dart';
import 'package:aibook/utils/resource.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:http/http.dart' as http;

class ResourcesList extends StatefulWidget {
  final Source source;
  final Color color;
  const ResourcesList({
    Key? key,
    required this.source,
    required this.color,
  }) : super(key: key);

  @override
  State<ResourcesList> createState() => _ResourcesListState();
}

class _ResourcesListState extends State<ResourcesList> {
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
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.source.title),
        backgroundColor: widget.color,
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: PagedListView<int, Resource>(
          pagingController: _pagingController,
          builderDelegate: PagedChildBuilderDelegate<Resource>(
            itemBuilder: (context, resource, index) =>
                ResourceItem(resource: resource),
          ),
        ),
      ),
    );
  }

  Future<void> _fetchPage(int pageKey) async {
    try {
      final response = await http.get(Uri.parse(
          "https://raw.githubusercontent.com/sleepingsaint/AI-Book/db/resources/${widget.source.id}/$pageKey.json"));
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
