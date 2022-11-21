import 'package:aibook/constants.dart';
import 'package:aibook/utils/source.dart';
import 'package:aibook/widgets/source_resources_list.dart';
import 'package:flutter/material.dart';

class SourceItem extends StatelessWidget {
  final Source source;
  const SourceItem({
    Key? key,
    required this.source,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      child: Card(
        color: colorPallete[source.id % colorPallete.length],
        child: Align(
          alignment: Alignment.bottomLeft,
          child: Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.bottomCenter,
                end: Alignment.topCenter,
                colors: [
                  Colors.black38,
                  Colors.black12,
                  Colors.transparent,
                ],
              ),
              borderRadius: BorderRadius.only(
                bottomLeft: Radius.circular(4.0),
                bottomRight: Radius.circular(4.0),
              ),
            ),
            child: ListTile(
              title: Text(
                source.title,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w500,
                ),
              ),
              subtitle: Text(
                "${source.numResources} Resources",
                style: const TextStyle(
                  color: Colors.white60,
                ),
              ),
            ),
          ),
        ),
      ),
      onTap: () => Navigator.of(context).push(
        MaterialPageRoute(
          builder: (context) => Scaffold(
            appBar: AppBar(
              title: Text(source.title),
              backgroundColor: colorPallete[source.id % colorPallete.length],
            ),
            body: SourceResourcesList(source: source),
          ),
        ),
      ),
    );
  }
}
