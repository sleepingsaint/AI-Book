import 'package:aibook/widgets/banner_cards.dart';
import 'package:aibook/widgets/latest_resources_list.dart';
import 'package:flutter/material.dart';
import 'package:flutter_sticky_header/flutter_sticky_header.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0.0,
        title: Padding(
          padding: const EdgeInsets.only(top: 8.0),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              IconButton(
                onPressed: () {},
                icon: Image.asset("assets/icons/icon.png"),
              ),
              Text(
                "AI Book",
                style: TextStyle(
                  color: Colors.black87,
                  fontSize: MediaQuery.of(context).textScaleFactor * 32,
                ),
              ),
            ],
          ),
        ),
        actions: [
          IconButton(
            onPressed: () =>
                Navigator.of(context).pushNamed("/bookmarkedResources"),
            icon: const Icon(Icons.bookmark, color: Color(0xFF3A3C41)),
          ),
        ],
      ),
      body: NestedScrollView(
        headerSliverBuilder: (context, innerBoxIsScrolled) => [
          SliverStickyHeader(
            sticky: false,
            header: const Padding(
              padding: EdgeInsets.only(left: 8.0, right: 8.0, top: 8.0),
              child: BannerCards(),
            ),
          ),
        ],
        body: Padding(
          padding: const EdgeInsets.all(8.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(
                  "Latest Resources",
                  style: TextStyle(
                    fontSize: MediaQuery.of(context).textScaleFactor * 24,
                  ),
                ),
              ),
              const Expanded(
                child: LatestResourcesList(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
