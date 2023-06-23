import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/pages/cart_page/cart_page.dart';
import 'package:kununua_app/pages/main_page/main_page.dart';
import 'package:kununua_app/pages/not_implemented_page.dart';
import 'package:kununua_app/pages/profile_page/profile_page.dart';
import 'package:kununua_app/pages/search_page/search_page.dart';
import 'package:kununua_app/pages/list_page/list_page.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/widgets/expandable_floating_action_button/expandable_floating_action_button.dart';
import 'package:kununua_app/widgets/expandable_floating_action_button/components/action_button.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

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
  Map<String, List<String>> _searchFiltersSetted = {};
  Map<String, List<String>> _searchOriginalFilters = {};
  List<dynamic> _searchProductsList = [];
  int _searchTotalResults = 0;


  void updateSearchProductsList(
      List<dynamic> productsList, Map<String, List<String>> filtersSetted) {
    setState(() {
      _searchProductsList = productsList;
      _searchFiltersSetted = filtersSetted;
      _searchTotalResults = productsList.length;
    });
  }

  void updateSearchFilters(
      List<dynamic> productsList,
      Map<String, List<String>> filtersSetted,
      Map<String, List<String>> originalFilters) {
    setState(() {
      _searchProductsList = productsList;
      _searchFiltersSetted = filtersSetted;
      _searchOriginalFilters = originalFilters;
      _searchTotalResults = productsList.length;
    });
  }

  @override
  void initState() {
    _currentScreen = widget.firstScreen;
    super.initState();
    _searchFiltersSetted = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': [],
    };
    _searchOriginalFilters = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': [],
      'Nombres': [],
    };
    _searchTotalResults = 0;
  }

  Widget _loadScreen(Screens screen) {
    switch (screen) {
      case Screens.home:
        return const MainPage();
      case Screens.stats:
        return const NotImplementedPage();
      case Screens.search:
        return SearchPage(
            productsList: _searchProductsList,
            updateFilters: updateSearchFilters,
            totalResults: _searchTotalResults);
      case Screens.list:
        return const ListPage();
      case Screens.profile:
        return const ProfilePage();
      case Screens.cart:
        return Container();
    }
  }

  PreferredSizeWidget? _loadAppBar(Screens screen) {
    switch (screen) {
      case Screens.home:
        return const MainPageAppBar(text: kHomeText, letterSpacing: 2.5);
      case Screens.stats:
        return const MainPageAppBar(text: kStatsText);
      case Screens.search:
        return MainPageAppBar(text: kSearchText, actions: [Container()]);
      case Screens.list:
        return const MainPageAppBar(text: kListText);
      case Screens.profile:
        return const MainPageAppBar(text: kProfileText);
      case Screens.cart:
        return null;
    }
  }

  currentScreenCallback(Screens screen) {
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
              updateProductsList: updateSearchProductsList,
              originalFilters: _searchOriginalFilters,
              settedFilters: _searchFiltersSetted,
            )
          : null,
      body: _loadScreen(_currentScreen),
      floatingActionButton: 
          FloatingActionButton(
              onPressed: () {
                Navigator.of(context).pushReplacement(
                                      MaterialPageRoute(
                                          builder: (context) =>
                                              const CartPage()));
              },
              backgroundColor: kPrimaryColor,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(50)),
              child: const Icon(Icons.shopping_cart),
            ),
      bottomNavigationBar: KununuaNavBar(
        screen: _currentScreen,
        currentScreenCallback: currentScreenCallback,
      ),
    );
  }
}
