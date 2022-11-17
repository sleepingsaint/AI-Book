import 'package:aibook/constants.dart';
import 'package:aibook/utils/resource.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:url_launcher/url_launcher.dart';

class ResourceItem extends StatelessWidget {
  final Resource resource;
  final bool showSource;
  const ResourceItem({
    Key? key,
    required this.resource,
    this.showSource = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
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
    );
  }

  Color _getBackgroundColor(Color color) {
    Color newColor = Color.fromRGBO(color.red, color.green, color.blue, 0.2);
    return newColor;
  }
}
