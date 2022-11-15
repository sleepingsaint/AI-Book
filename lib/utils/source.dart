class Source {
  final int id;
  final String title;
  final String url;
  final int numResources;

  Source({
    required this.id,
    required this.title,
    required this.url,
    required this.numResources,
  });

  factory Source.fromJSON(Map<String, dynamic> json) {
    return Source(
      id: json["id"],
      title: json["title"],
      url: json["url"],
      numResources: json["numResources"],
    );
  }
}
