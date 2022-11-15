import 'package:aibook/screens/resources_list.dart';
import 'package:aibook/screens/sources_list.dart';
import 'package:aibook/utils/resources_screen_arguments.dart';
import 'package:flutter/material.dart';

void main() {
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
          final args = settings.arguments as ResourceScreenArgs;
          return MaterialPageRoute(builder: (context) {
            return ResourcesList(
              source: args.source,
              color: args.color,
            );
          });
        }
        return MaterialPageRoute(builder: (context) {
          return const SourcesList();
        });
      },
    );
  }
}
