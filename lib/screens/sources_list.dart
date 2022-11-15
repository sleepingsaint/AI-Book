import 'dart:convert';

import 'package:aibook/screens/source_item.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';
import 'package:infinite_scroll_pagination/infinite_scroll_pagination.dart';
import 'package:http/http.dart' as http;

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

  final List<int> colors = [
    0xFF493657,
    0xFF328543,
    0xFF8C5A7E,
    0xFFA6B5A9,
    0xFFE85E4D,
    0xFF9F877F,
    0xFF5B6761,
    0xFF682747,
    0xFFF55200,
    0xFF3A3C41
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(
          "Sources",
          style: TextStyle(
            color: Colors.black54,
          ),
        ),
        elevation: 0.0,
        backgroundColor: Colors.white,
      ),
      body: Padding(
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
              color: Color(colors[idx % colors.length]),
            ),
          ),
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
