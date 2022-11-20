class Resource {
  final int id;
  final String title;
  final String url;
  final String? authors;
  final String? tags;
  final String? description;
  final String? thumbnail;
  final String? publishedOn;
  int? sourceId;
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
