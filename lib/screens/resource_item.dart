import 'package:aibook/utils/resource.dart';
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:link_preview_generator/link_preview_generator.dart';
import 'package:url_launcher/url_launcher.dart';

class ResourceItem extends StatefulWidget {
  final Resource resource;
  const ResourceItem({Key? key, required this.resource}) : super(key: key);

  @override
  State<ResourceItem> createState() => _ResourceItemState();
}

class _ResourceItemState extends State<ResourceItem> {
  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            FutureBuilder<WebInfo>(
              future: LinkPreview.scrapeFromURL(widget.resource.url),
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      ListTile(
                        contentPadding: const EdgeInsets.all(0.0),
                        title: Text(
                          widget.resource.title,
                          style: const TextStyle(fontWeight: FontWeight.w700),
                        ),
                        trailing: snapshot.data!.image.isNotEmpty
                            ? Image.network(
                                snapshot.data!.image,
                                height: 48.0,
                                width: 48.0,
                                fit: BoxFit.contain,
                                errorBuilder: ((context, error, stackTrace) =>
                                    const SizedBox.shrink()),
                              )
                            : const SizedBox.shrink(),
                        onTap: () => launchUrl(
                          Uri.parse(
                            widget.resource.url
                                .replaceAll("https", "http")
                                .replaceAll("http", "https"),
                          ),
                          mode: LaunchMode.externalApplication,
                        ),
                      ),
                      snapshot.data!.description.isNotEmpty
                          ? Text(
                              snapshot.data!.description,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            )
                          : const SizedBox.shrink(),
                      const SizedBox(height: 10.0),
                    ],
                  );
                }
                return ListTile(
                  contentPadding: const EdgeInsets.all(0.0),
                  title: Text(
                    widget.resource.title,
                    style: const TextStyle(fontWeight: FontWeight.w700),
                  ),
                  onTap: () => launchUrl(
                    Uri.parse(
                      widget.resource.url
                          .replaceAll("https", "http")
                          .replaceAll("http", "https"),
                    ),
                    mode: LaunchMode.externalApplication,
                  ),
                );
              },
            ),
            Text(
              "Published On ${DateFormat('d MMMM, y').format(DateTime.parse(widget.resource.publishedOn))}",
              style: TextStyle(
                  fontWeight: FontWeight.bold, color: Colors.grey.shade600),
            ),
          ],
        ),
      ),
    );
  }
}
