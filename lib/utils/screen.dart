import 'package:flutter/material.dart';

class ScreenProvider extends ChangeNotifier {
  int _selectedIndex = 0;

  int get selectedIndex => _selectedIndex;

  void moveToScreen(int idx) {
    _selectedIndex = idx;
    notifyListeners();
  }
}
