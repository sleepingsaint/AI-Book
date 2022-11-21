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
        title: const Text("AI Book"),
        backgroundColor: const Color(0xFF493657),
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
          SliverStickyHeader(
            sticky: true,
            header: Padding(
              padding: const EdgeInsets.only(top: 8.0, left: 12.0, bottom: 8.0),
              child: Text(
                "Latest Resources",
                style: TextStyle(
                  fontSize: MediaQuery.of(context).textScaleFactor * 24,
                ),
              ),
            ),
          ),
        ],
        body: const Padding(
          padding: EdgeInsets.all(6.0),
          child: LatestResourcesList(),
        ),
      ),
    );
  }
}
