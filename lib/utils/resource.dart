import 'package:hive/hive.dart';

part 'resource.g.dart';

@HiveType(typeId: 1)
class Resource {
  @HiveField(0)
  final int id;

  @HiveField(1)
  final String title;

  @HiveField(2)
  final String url;

  @HiveField(3)
  final String? authors;

  @HiveField(4)
  final String? tags;

  @HiveField(5)
  final String? description;

  @HiveField(6)
  final String? thumbnail;

  @HiveField(7)
  final String? publishedOn;

  @HiveField(8)
  int? sourceId;

  @HiveField(9)
  String? source;

  Resource({
    required this.id,
    required this.title,
    required this.url,
    this.publishedOn,
    this.authors,
    this.tags,
    this.description,
    this.thumbnail,
    this.sourceId,
    this.source,
  });

  factory Resource.fromJSON(Map<String, dynamic> json) {
    return Resource(
      id: json["id"],
      title: json["title"],
      url: json["url"],
      authors: json["authors"],
      tags: json["tags"],
      publishedOn: json["publishedOn"],
      description: json["description"],
      thumbnail: json["thumbnail"],
      sourceId: json["sourceId"],
      source: json["source"],
    );
  }
}
