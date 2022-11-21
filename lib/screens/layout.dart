import 'package:aibook/screens/all_resources_screen.dart';
import 'package:aibook/screens/bookmarked_resources_screen.dart';
import 'package:aibook/screens/home_screen.dart';
import 'package:aibook/screens/sources_screen.dart';
import 'package:aibook/utils/screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class ScreenConfig {
  final String title;
  final Color color;

  ScreenConfig({
    required this.title,
    required this.color,
  });
}

class NavigatorPage extends StatelessWidget {
  final Widget child;
  final GlobalKey globalKey;
  const NavigatorPage({
    Key? key,
    required this.child,
    required this.globalKey,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: globalKey,
      onGenerateRoute: (settings) {
        return MaterialPageRoute(builder: (context) => child);
      },
    );
  }
}

class Layout extends StatelessWidget {
  Layout({Key? key}) : super(key: key);

  final List<GlobalKey> globalKeys = [
    GlobalKey(),
    GlobalKey(),
    GlobalKey(),
    GlobalKey(),
  ];

  @override
  Widget build(BuildContext context) {
    int selectedIndex = Provider.of<ScreenProvider>(context).selectedIndex;
    return Scaffold(
      body: WillPopScope(
        onWillPop: () async {
          return !await Navigator.maybePop(
              globalKeys[selectedIndex].currentState!.context);
        },
        child: IndexedStack(index: selectedIndex, children: [
          NavigatorPage(
            globalKey: globalKeys[0],
            child: const HomeScreen(),
          ),
          NavigatorPage(
            globalKey: globalKeys[1],
            child: const SourcesScreen(),
          ),
          NavigatorPage(
            globalKey: globalKeys[2],
            child: const AllResourcesScreen(),
          ),
          NavigatorPage(
            globalKey: globalKeys[3],
            child: const BookmarkedResourcesScreen(),
          ),
        ]),
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
        selectedItemColor: Colors.blueGrey.shade500,
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
