import 'package:aibook/utils/resources_screen_arguments.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';

class SourceItem extends StatelessWidget {
  final Source source;
  final Color color;
  const SourceItem({
    Key? key,
    required this.source,
    required this.color,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      child: Card(
        color: color,
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
      onTap: () => Navigator.of(context).pushNamed(
        "/resources",
        arguments: ResourceScreenArgs(
          source: source,
          color: color,
        ),
      ),
    );
  }
}
