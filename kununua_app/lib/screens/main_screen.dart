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
  final GlobalKey<FormState> _formkey = GlobalKey<FormState>();
  late Screens _currentScreen;
  late int? maxSupermarkets;
  String listName = '';
  Map<String, List<String>> _searchFilters = {};
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
      Map<String, List<String>> filters,
      Map<String, List<String>> filtersSetted,
      Map<String, List<String>> originalFilters) {
    setState(() {
      _searchProductsList = productsList;
      _searchFiltersSetted = filtersSetted;
      _searchFilters = filters;
      _searchOriginalFilters = originalFilters;
      _searchTotalResults = productsList.length;
    });
  }

  @override
  void initState() {
    _currentScreen = widget.firstScreen;
    super.initState();
    maxSupermarkets = null;
    _searchFilters = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': [],
    };
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
      case Screens.cart:
        return const CartPage();
      case Screens.list:
        return const ListPage();
      case Screens.profile:
        return const ProfilePage();
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
      case Screens.cart:
        return const MainPageAppBar(text: kCartText);
      case Screens.list:
        return const MainPageAppBar(text: kListText);
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

  Future<bool> _createList(String listName) async {
    debugPrint(listName);
    final MutationOptions createListMutation = MutationOptions(
      document: gql(createList),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
        'listName': listName,
      },
    );

    final entryResult = await globals.client.value.mutate(createListMutation);

    return !entryResult.hasException;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: _loadAppBar(_currentScreen),
      endDrawer: _currentScreen == Screens.search
          ? ProductGridFilters(
              filters: _searchFilters,
              updateProductsList: updateSearchProductsList,
              originalFilters: _searchOriginalFilters,
              settedFilters: _searchFiltersSetted,
            )
          : null,
      body: _loadScreen(_currentScreen),
      floatingActionButton: _currentScreen != Screens.cart
          ? FloatingActionButton(
              onPressed: () {
                currentScreenCallback(Screens.cart);
              },
              backgroundColor: kPrimaryColor,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(50)),
              child: const Icon(Icons.shopping_cart),
            )
          : ExpandableFab(
              backgroundColor: kPrimaryColor,
              icon: const Icon(Icons.format_list_bulleted_outlined),
              borderRadius: BorderRadius.circular(15),
              children: [
                ActionButton(
                  onPressed: () {
                    showModalBottomSheet<void>(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(25.0),
                      ),
                      context: context,
                      builder: (BuildContext context) {
                        return Container(
                          height: 400,
                          padding: const EdgeInsets.symmetric(horizontal: 20.0),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(25.0),
                            color: Colors.white,
                          ),
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
                                      style: TextStyle(
                                        fontSize: 16,
                                      )),
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
                                    labelText: "Número máximo de supermercados",
                                    labelStyle: TextStyle(
                                        overflow: TextOverflow.ellipsis),
                                  ),
                                  onChanged: (value) {
                                    setState(() {
                                      maxSupermarkets = int.tryParse(value);
                                    });
                                  },
                                ),
                                Button(
                                  text: "OPTIMIZAR",
                                  paddingContainer:
                                      const EdgeInsets.fromLTRB(75, 25, 75, 10),
                                  action: () {
                                    _upgradeCartRequest(maxSupermarkets)
                                        .then((edited) {
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
                                        ScaffoldMessenger.of(context)
                                            .showSnackBar(
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
                  icon: const Icon(Icons.insights_rounded),
                  borderRadius: BorderRadius.circular(50),
                ),
                ActionButton(
                  onPressed: () {
                    showModalBottomSheet<void>(
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(25.0),
                      ),
                      context: context,
                      builder: (BuildContext context) {
                        return Container(
                          height: 400,
                          padding: const EdgeInsets.symmetric(horizontal: 20.0),
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(25.0),
                            color: Colors.white,
                          ),
                          child: Center(
                            child: Form(
                              key: _formkey,
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                mainAxisSize: MainAxisSize.max,
                                children: <Widget>[
                                  Container(
                                    margin: const EdgeInsets.only(bottom: 20.0),
                                    child: const Text(
                                        "Por favor, escriba un nombre para la lista que está a punto de crear",
                                        textAlign: TextAlign.center,
                                        style: TextStyle(
                                          fontSize: 16,
                                        )),
                                  ),
                                  TextFormField(
                                    validator: (value) {
                                      if (value == null ||
                                          value.isEmpty ||
                                          value.trim().isEmpty) {
                                        return 'Por favor ingrese un valor';
                                      } else if (value.length > 64) {
                                        return 'El nombre debe tener menos de 64 caracteres';
                                      }
                                      return null;
                                    },
                                    keyboardType: TextInputType.name,
                                    decoration: const InputDecoration(
                                      labelText: "Nombre de la lista",
                                      labelStyle: TextStyle(
                                          overflow: TextOverflow.ellipsis),
                                    ),
                                    onChanged: (value) {
                                      setState(() {
                                        listName = value;
                                      });
                                    },
                                    maxLines: 1,
                                    minLines: 1,
                                    autocorrect: true,
                                  ),
                                  Button(
                                    paddingContainer: const EdgeInsets.fromLTRB(
                                        75, 25, 75, 10),
                                    text: "CREAR LISTA",
                                    action: () {
                                      final isvalid =
                                          _formkey.currentState!.validate();
                                      if (isvalid) {
                                        _formkey.currentState!.save();
                                        _createList(listName).then((edited) {
                                          Navigator.of(context).pop();
                                          if (edited) {
                                            Navigator.of(context)
                                                .pushReplacement(
                                              MaterialPageRoute(
                                                  builder: (context) =>
                                                      const MainScreen(
                                                        firstScreen:
                                                            Screens.cart,
                                                      )),
                                            );
                                          } else {
                                            ScaffoldMessenger.of(context)
                                                .showSnackBar(
                                              const SnackBar(
                                                content: Text(
                                                    "Ha ocurrido un error. Vuelva a intentarlo más tarde."),
                                              ),
                                            );
                                          }
                                        });
                                      }
                                    },
                                    color: kPrimaryColor,
                                  )
                                ],
                              ),
                            ),
                          ),
                        );
                      },
                    );
                  },
                  icon: const Icon(Icons.add),
                  backgroundColor: kPrimaryColor,
                  borderRadius: BorderRadius.circular(50),
                ),
              ],
            ),
      bottomNavigationBar: KununuaNavBar(
        screen: _currentScreen,
        currentScreenCallback: currentScreenCallback,
      ),
    );
  }
}
