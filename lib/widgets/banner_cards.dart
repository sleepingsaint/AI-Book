import 'dart:convert';
import 'package:aibook/constants.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:intl/intl.dart';

class BannerCardTile extends StatelessWidget {
  final int title;
  final String subtitle;
  final int colorIdx;
  final String path;

  const BannerCardTile({
    Key? key,
    required this.title,
    required this.subtitle,
    required this.colorIdx,
    required this.path,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      child: Card(
        color: colorPallete[colorIdx],
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
                NumberFormat.compactLong()
                    .format(title)
                    .replaceAll("thousand", "K"),
                style: TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w500,
                  fontSize: MediaQuery.of(context).textScaleFactor * 24.0,
                ),
              ),
              subtitle: Text(
                subtitle,
                style: const TextStyle(
                  color: Colors.white60,
                ),
              ),
            ),
          ),
        ),
      ),
      onTap: () => Navigator.of(context).pushNamed(path),
    );
  }
}

class BannerCards extends StatelessWidget {
  const BannerCards({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: _getInfo(),
      builder: (context, snapshot) {
        if (snapshot.hasData) {
          return GridView.count(
            shrinkWrap: true,
            crossAxisCount: 2,
            children: [
              BannerCardTile(
                title: snapshot.data!["numSources"],
                subtitle: "Sources",
                colorIdx: 0,
                path: "/sources",
              ),
              BannerCardTile(
                title: snapshot.data!["numResources"],
                subtitle: "Resources",
                colorIdx: 1,
                path: "/allResources",
              ),
            ],
          );
          // return BannerCardTile(
          //   title: snapshot.data!["numSources"].toString(),
          //   subtitle: "Sources",
          // );
        }
        if (snapshot.hasError) {
          return const Text("Oops! Something went wrong");
        }
        return const Center(child: CircularProgressIndicator());
      },
    );
  }

  Future<Map<String, dynamic>> _getInfo() async {
    const String endpoint =
        "https://raw.githubusercontent.com/sleepingsaint/AI-Book/db/info.json";
    final response = await http.get(Uri.parse(endpoint));

    if (response.statusCode == 200) {
      Map<String, dynamic> data = jsonDecode(response.body);
      return data;
    }
    return {};
  }
}
