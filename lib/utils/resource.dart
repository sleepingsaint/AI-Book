class Resource {
  final int id;
  final String title;
  final String url;
  final String? authors;
  final String? tags;
  final String publishedOn;

  Resource({
    required this.id,
    required this.title,
    required this.url,
    required this.publishedOn,
    this.authors,
    this.tags,
  });

  factory Resource.fromJSON(Map<String, dynamic> json) {
    return Resource(
      id: json["id"],
      title: json["title"],
      url: json["url"],
      authors: json["authors"],
      tags: json["tags"],
      publishedOn: json["publishedOn"],
    );
  }
}
