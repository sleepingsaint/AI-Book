import 'package:aibook/constants.dart';
import 'package:aibook/utils/database.dart';
import 'package:aibook/utils/resource.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';
import 'package:flutter_slidable/flutter_slidable.dart';
import 'package:hive/hive.dart';
import 'package:intl/intl.dart';
import 'package:share_plus/share_plus.dart';
import 'package:url_launcher/url_launcher.dart';

class ResourceItem extends StatelessWidget {
  final Resource resource;
  final bool showSource;
  ResourceItem({
    Key? key,
    required this.resource,
    this.showSource = false,
  }) : super(key: key);

  final DatabaseClient client = DatabaseClient();

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(
        bottom: 8.0,
        left: 8.0,
        right: 8.0,
      ),
      child: Slidable(
        key: ValueKey(resource.id),
        endActionPane: ActionPane(motion: const ScrollMotion(), children: [
          ValueListenableBuilder<Box<Resource>>(
            valueListenable: client.getListenable(resource.id),
            builder: (context, box, child) {
              Resource? result = box.get(resource.id);
              return SlidableAction(
                onPressed: (context) async {
                  if (box.get(resource.id) == null) {
                    box.put(resource.id, resource);
                  } else {
                    box.delete(resource.id);
                  }
                },
                backgroundColor: result != null
                    ? const Color.fromARGB(255, 76, 116, 151)
                    : const Color.fromARGB(100, 76, 116, 151),
                foregroundColor: Colors.white,
                icon: Icons.bookmark_add,
                label: result != null ? "Saved" : "Save",
              );
            },
          ),
          SlidableAction(
            onPressed: (context) {
              Share.share(
                resource.url,
                subject: resource.title,
              );
            },
            backgroundColor: const Color.fromARGB(255, 66, 176, 79),
            foregroundColor: Colors.white,
            icon: Icons.share,
            label: 'Share',
          ),
        ]),
        child: Card(
          margin: const EdgeInsets.all(0.0),
          child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                GestureDetector(
                  onTap: () => launchUrl(
                    Uri.parse(resource.url),
                    mode: LaunchMode.externalApplication,
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(0.0),
                    title: Text(
                      resource.title,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                    trailing: (resource.thumbnail != null &&
                            resource.thumbnail!.isNotEmpty)
                        ? Image.network(resource.thumbnail!)
                        : const SizedBox.shrink(),
                  ),
                ),
                resource.description != null && resource.description!.isNotEmpty
                    ? Padding(
                        padding: const EdgeInsets.symmetric(vertical: 6.0),
                        child: Text(
                          resource.description!,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      )
                    : const SizedBox.shrink(),
                showSource && resource.source != null
                    ? GestureDetector(
                        onTap: () => Navigator.of(context).pushNamed(
                          "/resources",
                          arguments: Source(
                            id: resource.sourceId!,
                            title: resource.source!,
                            url: "",
                            numResources: -1,
                          ),
                        ),
                        child: Chip(
                          label: Text(resource.source!),
                          backgroundColor: _getBackgroundColor(colorPallete[
                              resource.sourceId! % colorPallete.length]),
                        ),
                      )
                    : const SizedBox.shrink(),
                resource.publishedOn != null && resource.publishedOn!.isNotEmpty
                    ? Text(
                        "Published On ${DateFormat('d MMMM, y').format(DateTime.parse(resource.publishedOn!))}",
                        style: TextStyle(
                          fontWeight: FontWeight.bold,
                          color: Colors.grey.shade600,
                        ),
                      )
                    : const SizedBox.shrink(),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Color _getBackgroundColor(Color color) {
    Color newColor = Color.fromRGBO(color.red, color.green, color.blue, 0.2);
    return newColor;
  }
}
