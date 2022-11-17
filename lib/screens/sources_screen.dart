import 'package:aibook/constants.dart';
import 'package:aibook/widgets/sources_list.dart';
import 'package:flutter/material.dart';

class SourcesScreen extends StatelessWidget {
  const SourcesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Sources"),
        backgroundColor: colorPallete[0],
      ),
      body: const Padding(
        padding: EdgeInsets.all(8.0),
        child: SourcesList(),
      ),
    );
  }
}
