import 'package:aibook/widgets/banner_cards.dart';
import 'package:aibook/widgets/latest_resources_list.dart';
import 'package:flutter/material.dart';

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
          child: Text(
            "AI Book",
            style: TextStyle(
              color: Colors.black87,
              fontSize: MediaQuery.of(context).textScaleFactor * 36,
            ),
          ),
        ),
      ),
      body: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const BannerCards(),
            const SizedBox(height: 12.0),
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
    );
  }
}
