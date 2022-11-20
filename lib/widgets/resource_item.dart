import 'package:aibook/constants.dart';
import 'package:aibook/utils/database.dart';
import 'package:aibook/utils/resource.dart';
import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';
import 'package:flutter_slidable/flutter_slidable.dart';
import 'package:intl/intl.dart';
import 'package:share_plus/share_plus.dart';
import 'package:url_launcher/url_launcher.dart';

class ResourceItem extends StatefulWidget {
  final Resource resource;
  final bool showSource;
  const ResourceItem({
    Key? key,
    required this.resource,
    this.showSource = false,
  }) : super(key: key);

  @override
  State<ResourceItem> createState() => _ResourceItemState();
}

class _ResourceItemState extends State<ResourceItem> {
  bool bookmarked = false;

  @override
  void initState() {
    setState(() {
      DatabaseHelper helper = DatabaseHelper();
      helper.checkResource(widget.resource).then((value) {
        setState(() {
          bookmarked = value;
        });
      });
    });
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(
        bottom: 8.0,
        left: 8.0,
        right: 8.0,
      ),
      child: Slidable(
        key: ValueKey(widget.resource.id),
        endActionPane: ActionPane(motion: const ScrollMotion(), children: [
          SlidableAction(
            onPressed: (context) async {
              DatabaseHelper helper = DatabaseHelper();
              if (!bookmarked) {
                bool result = await helper.addResource(widget.resource);
                setState(() {
                  bookmarked = result;
                });
              } else {
                bool result = await helper.removeResource(widget.resource);
                if (result) {
                  setState(() {
                    bookmarked = false;
                  });
                }
              }
            },
            backgroundColor: bookmarked
                ? const Color.fromARGB(255, 76, 116, 151)
                : const Color.fromARGB(100, 76, 116, 151),
            foregroundColor: Colors.white,
            icon: Icons.bookmark_add,
            label: 'Save',
          ),
          SlidableAction(
            onPressed: (context) {
              Share.share(
                widget.resource.url,
                subject: widget.resource.title,
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
                    Uri.parse(widget.resource.url),
                    mode: LaunchMode.externalApplication,
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.all(0.0),
                    title: Text(
                      widget.resource.title,
                      style: const TextStyle(fontWeight: FontWeight.w700),
                    ),
                    trailing: (widget.resource.thumbnail != null &&
                            widget.resource.thumbnail!.isNotEmpty)
                        ? Image.network(widget.resource.thumbnail!)
                        : const SizedBox.shrink(),
                  ),
                ),
                widget.resource.description != null &&
                        widget.resource.description!.isNotEmpty
                    ? Padding(
                        padding: const EdgeInsets.symmetric(vertical: 6.0),
                        child: Text(
                          widget.resource.description!,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                        ),
                      )
                    : const SizedBox.shrink(),
                widget.showSource && widget.resource.source != null
                    ? GestureDetector(
                        onTap: () => Navigator.of(context).pushNamed(
                          "/resources",
                          arguments: Source(
                            id: widget.resource.sourceId!,
                            title: widget.resource.source!,
                            url: "",
                            numResources: -1,
                          ),
                        ),
                        child: Chip(
                          label: Text(widget.resource.source!),
                          backgroundColor: _getBackgroundColor(colorPallete[
                              widget.resource.sourceId! % colorPallete.length]),
                        ),
                      )
                    : const SizedBox.shrink(),
                widget.resource.publishedOn != null &&
                        widget.resource.publishedOn!.isNotEmpty
                    ? Text(
                        "Published On ${DateFormat('d MMMM, y').format(DateTime.parse(widget.resource.publishedOn!))}",
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
