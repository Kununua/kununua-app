import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/pages/cart_page/cart_page.dart';
import 'package:kununua_app/pages/main_page/main_page.dart';
import 'package:kununua_app/pages/not_implemented_page.dart';
import 'package:kununua_app/pages/profile_page/profile_page.dart';
import 'package:kununua_app/pages/search_page/search_page.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/requests.dart';
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
  late int? maxSupermarkets;

  @override
  void initState() {
    _currentScreen = widget.firstScreen;
    super.initState();
    maxSupermarkets = null;
  }

  Widget _loadScreen(Screens screen) {
    switch (screen) {
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

  PreferredSizeWidget? _loadAppBar(Screens screen) {
    switch (screen) {
      case Screens.home:
        return const MainPageAppBar(text: kHomeText);
      case Screens.stats:
        return const MainPageAppBar(text: kStatsText);
      case Screens.search:
        return MainPageAppBar(text: kSearchText, actions: [Container()]);
      case Screens.cart:
        return const MainPageAppBar(text: kCartText);
      case Screens.profile:
        return const MainPageAppBar(text: kProfileText);
    }
  }

  currentScreenCallback(Screens screen) {
    setState(() {
      _currentScreen = screen;
    });
  }

  Future<bool> _upgradeCartRequest(int? maxSupermarkets) async {
    final MutationOptions upgradeCartOptions = MutationOptions(
      document: gql(upgradeCart),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
        'maxSupermarkets': maxSupermarkets,
      },
    );

    final entryResult = await globals.client.value.mutate(upgradeCartOptions);

    return !entryResult.hasException;
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
      floatingActionButton: _currentScreen != Screens.cart
          ? FloatingActionButton(
              onPressed: () {
                currentScreenCallback(Screens.cart);
              },
              backgroundColor: kPrimaryColor,
              child: const Icon(Icons.shopping_cart),
            )
          : FloatingActionButton(
              onPressed: () {
                showModalBottomSheet<void>(
                  context: context,
                  builder: (BuildContext context) {
                    return Container(
                      height: 400,
                      padding: const EdgeInsets.symmetric(horizontal: 20.0),
                      color: Colors.white,
                      child: Center(
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.center,
                          mainAxisSize: MainAxisSize.max,
                          children: <Widget>[
                            Container(
                              margin: const EdgeInsets.only(bottom: 20.0),
                              child: const Text(
                                "Por favor, introduzca el número máximo de supermercados entre los que optimizar, en caso de quiera limitar el número de supermercados a los que ir",
                                textAlign: TextAlign.center,
                              ),
                            ),
                            TextFormField(
                              validator: (value) {
                                if (value == null || value.isEmpty) {
                                  return 'Por favor ingrese un valor';
                                } else if (int.tryParse(value) == null) {
                                  return 'Por favor ingrese un valor numérico';
                                } else if (int.tryParse(value)! < 1) {
                                  return 'Por favor ingrese un valor mayor o igual a 1';
                                }
                                return null;
                              },
                              keyboardType: TextInputType.number,
                              decoration: const InputDecoration(
                                labelText:
                                    "Máximos supermercados entre los que optimizar",
                              ),
                              onChanged: (value) {
                                setState(() {
                                  maxSupermarkets = int.tryParse(value);
                                });
                              },
                            ),
                            Button(
                              text: "OPTIMIZAR",
                              action: () {
                                _upgradeCartRequest(maxSupermarkets).then((edited) {
                                  Navigator.of(context).pop();
                                  if (edited) {
                                    Navigator.of(context).pushReplacement(
                                      MaterialPageRoute(
                                          builder: (context) =>
                                              const MainScreen(
                                                firstScreen: Screens.cart,
                                              )),
                                    );
                                  } else {
                                    ScaffoldMessenger.of(context).showSnackBar(
                                      const SnackBar(
                                        content: Text(
                                            "El carrito ya es lo más optimo posible"),
                                      ),
                                    );
                                  }
                                });
                              },
                              color: kPrimaryColor,
                            )
                          ],
                        ),
                      ),
                    );
                  },
                );
              },
              backgroundColor: kPrimaryColor,
              child: const Icon(Icons.insights_rounded),
            ),
      bottomNavigationBar: KununuaNavBar(
        screen: _currentScreen,
        currentScreenCallback: currentScreenCallback,
      ),
    );
  }
}
