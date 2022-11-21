import 'package:aibook/widgets/all_resources_list.dart';
import 'package:flutter/material.dart';

class AllResourcesScreen extends StatelessWidget {
  const AllResourcesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("All Resources"),
        backgroundColor: const Color(0xFF8C5A7E),
      ),
      body: const AllResourcesList(),
    );
  }
}
