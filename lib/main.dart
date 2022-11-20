import 'package:aibook/screens/all_resources_screen.dart';
import 'package:aibook/screens/home_screen.dart';
import 'package:aibook/screens/bookmarked_resources_screen.dart';
import 'package:aibook/screens/source_resources_screen.dart';
import 'package:aibook/screens/sources_screen.dart';
import 'package:aibook/utils/database.dart';

import 'package:aibook/utils/source.dart';
import 'package:flutter/material.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await DatabaseHelper.initDB();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "AI Book",
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      initialRoute: "/",
      onGenerateRoute: (settings) {
        if (settings.name == "/resources") {
          final args = settings.arguments as Source;
          return MaterialPageRoute(builder: (context) {
            return SourceResourcesScreen(source: args);
          });
        }
      },
      routes: {
        "/": (context) => const HomeScreen(),
        "/sources": (context) => const SourcesScreen(),
        "/allResources": (context) => const AllResourcesScreen(),
        "/bookmarkedResources": (context) => const BookmarkedResourcesScreen(),
      },
    );
  }
}
