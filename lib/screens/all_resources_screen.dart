import 'package:aibook/constants.dart';
import 'package:aibook/widgets/all_resources_list.dart';
import 'package:flutter/material.dart';

class AllResourcesScreen extends StatelessWidget {
  const AllResourcesScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("All Resources"),
        backgroundColor: colorPallete[1],
      ),
      body: const AllResourcesList(),
    );
  }
}
