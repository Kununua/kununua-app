import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/pages/cart_page/cart_page.dart';
import 'package:kununua_app/pages/main_page/main_page.dart';
import 'package:kununua_app/pages/not_implemented_page.dart';
import 'package:kununua_app/pages/profile_page/profile_page.dart';
import 'package:kununua_app/pages/search_page/search_page.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';

class MainScreen extends StatefulWidget {

  final Screens firstScreen;

  const MainScreen({
    super.key,
    this.firstScreen = Screens.home,
  });

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {

  late Screens _currentScreen;

  @override
  void initState() {
    _currentScreen = widget.firstScreen;
    super.initState();
  }

  Widget _loadScreen(Screens screen){
    switch(screen){
      case Screens.home:
        return const MainPage();
      case Screens.stats:
        return const NotImplementedPage();
      case Screens.search:
        return const SearchPage();
      case Screens.cart:
        return const CartPage();
      case Screens.profile:
        return const ProfilePage();
    }
  }

  PreferredSizeWidget? _loadAppBar(Screens screen){
    switch(screen){
      case Screens.home:
        return const MainPageAppBar(
          text: kHomeText
        );
      case Screens.stats:
        return const MainPageAppBar(
          text: kStatsText
        );
      case Screens.search:
        return MainPageAppBar(text: kSearchText, actions: [Container()]
        );
      case Screens.cart:
        return const MainPageAppBar(
          text: kCartText
        );
      case Screens.profile:
        return const MainPageAppBar(
          text: kProfileText
        );
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
      endDrawer: _currentScreen == Screens.search
          ? ProductGridFilters(
              updateProductsList: () => {},
            )
          : null,
      body: _loadScreen(_currentScreen),
      bottomNavigationBar: KununuaNavBar(
        screen: _currentScreen,
        currentScreenCallback: currentScreenCallback,
      ),
    );
  }
}