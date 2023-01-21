import 'package:flutter/material.dart';
import 'package:kununua_app/screens/main_screen/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/screens/main_screen/sub_screens_widgets/main_page.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';
import 'package:kununua_app/screens/welcome_screen/welcome_screen.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {

  Screens _currentScreen = Screens.home;

  Widget _loadScreen(Screens screen){
    switch(screen){
      case Screens.home:
        return const MainPage();
      case Screens.stats:
        return const WelcomeScreen();
      case Screens.search:
        return const MainPage();
      case Screens.cart:
        return const MainPage();
      case Screens.profile:
        return const MainPage();
    }
  }

  PreferredSizeWidget? _loadAppBar(Screens screen){
    switch(screen){
      case Screens.home:
        return const MainPageAppBar();
      case Screens.stats:
        return const MainPageAppBar();
      case Screens.search:
        return const MainPageAppBar();
      case Screens.cart:
        return const MainPageAppBar();
      case Screens.profile:
        return const MainPageAppBar();
    }
  }

  currentScreenCallback(Screens screen){
    setState(() {
      _currentScreen = screen;
    });
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: _loadAppBar(_currentScreen),
      body: _loadScreen(_currentScreen),
      bottomNavigationBar: KununuaNavBar(
        screen: _currentScreen,
        currentScreenCallback: currentScreenCallback,
      ),
    );
  }
}