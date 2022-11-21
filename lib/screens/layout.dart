import 'package:aibook/constants.dart';
import 'package:aibook/screens/home_screen.dart';
import 'package:aibook/utils/screen.dart';
import 'package:aibook/widgets/all_resources_list.dart';
import 'package:aibook/widgets/bookmarked_resources_list.dart';
import 'package:aibook/widgets/sources_list.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ScreenConfig {
  final String title;
  final Color color;
  final Widget body;

  ScreenConfig({
    required this.title,
    required this.color,
    required this.body,
  });
}

class Layout extends StatelessWidget {
  Layout({Key? key}) : super(key: key);

  final List<ScreenConfig> screenConfigs = [
    ScreenConfig(
      title: "AI Book",
      color: colorPallete[0],
      body: const HomeScreen(),
    ),
    ScreenConfig(
      title: "Sources",
      color: colorPallete[1],
      body: const SourcesList(),
    ),
    ScreenConfig(
      title: "Resources",
      color: colorPallete[2],
      body: const AllResourcesList(),
    ),
    ScreenConfig(
      title: "Bookmarked Resources",
      color: colorPallete[8],
      body: BookmarkedResourcesList(),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    int selectedIndex = Provider.of<ScreenProvider>(context).selectedIndex;
    return Scaffold(
      appBar: AppBar(
        title: Text(screenConfigs[selectedIndex].title),
        backgroundColor: screenConfigs[selectedIndex].color,
      ),
      body: IndexedStack(
        index: selectedIndex,
        children: screenConfigs.map((config) => config.body).toList(),
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: "Home",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.source),
            label: "Sources",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.article),
            label: "Resources",
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bookmark),
            label: "Bookmarked",
          ),
        ],
        currentIndex: selectedIndex,
        showUnselectedLabels: true,
        unselectedItemColor: Colors.grey.shade900,
        selectedItemColor: screenConfigs[selectedIndex].color,
        onTap: (value) {
          Provider.of<ScreenProvider>(
            context,
            listen: false,
          ).moveToScreen(value);
        },
      ),
    );
  }
}
