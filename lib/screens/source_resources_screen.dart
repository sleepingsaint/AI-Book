import 'package:aibook/constants.dart';
import 'package:aibook/utils/source.dart';
import 'package:aibook/widgets/source_resources_list.dart';
import 'package:flutter/material.dart';

class SourceResourcesScreen extends StatelessWidget {
  final Source source;
  const SourceResourcesScreen({Key? key, required this.source})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(source.title),
        backgroundColor: colorPallete[source.id % colorPallete.length],
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: SourceResourcesList(
          source: source,
        ),
      ),
    );
  }
}
