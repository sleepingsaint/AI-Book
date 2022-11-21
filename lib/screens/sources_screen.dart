import 'package:aibook/widgets/sources_list.dart';
import 'package:flutter/material.dart';

class SourcesScreen extends StatelessWidget {
  const SourcesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Sources"),
        backgroundColor: const Color(0xFF328543),
      ),
      body: const SourcesList(),
    );
  }
}
