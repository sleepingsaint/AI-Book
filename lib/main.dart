import 'package:aibook/screens/layout.dart';
import 'package:aibook/utils/database.dart';
import 'package:aibook/utils/screen.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await DatabaseClient.initDB();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider<ScreenProvider>(
          create: (context) => ScreenProvider(),
        ),
      ],
      child: const MyApp(),
    ),
  );
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
      home: Layout(),
      // initialRoute: "/",
      // onGenerateRoute: (settings) {
      //   if (settings.name == "/resources") {
      //     final args = settings.arguments as Source;
      //     return MaterialPageRoute(builder: (context) {
      //       return SourceResourcesScreen(source: args);
      //     });
      //   }
      // },
      // routes: {
      //   "/": (context) => const HomeScreen(),
      //   "/sources": (context) => const SourcesScreen(),
      //   "/allResources": (context) => const AllResourcesScreen(),
      //   "/bookmarkedResources": (context) => const BookmarkedResourcesScreen(),
      // },
    );
  }
}
