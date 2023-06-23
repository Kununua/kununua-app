import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/pages/cart_page/components/cart_product.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:kununua_app/widgets/expandable_floating_action_button/components/action_button.dart';
import 'package:kununua_app/widgets/expandable_floating_action_button/expandable_floating_action_button.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';

class CartPage extends StatefulWidget {
  const CartPage({
    super.key,
  });

  @override
  State<CartPage> createState() => _CartPageState();
}

class _CartPageState extends State<CartPage> {
  late int? maxSupermarkets;
  String listName = '';
  final GlobalKey<FormState> _formkey = GlobalKey<FormState>();
  double _cartTotal = 0;
  bool _dataFetched = false;
  List<Map<String, dynamic>>? _products;

  @override
  void initState() {
    super.initState();
    maxSupermarkets = null;
  }

  void addPriceToTotal(double price) {
    setState(() {
      _cartTotal += price;
    });
  }

  Future<void> _getProductsInCart() async {
    
    if (!_dataFetched) {

      List<Map<String, dynamic>> products = [];

      final MutationOptions getProductsInCartOptions = MutationOptions(
        document: gql(getProductsInCart),
        variables: <String, dynamic>{
          'userToken': globals.prefs!.getString('jwtToken'),
        },
      );

      final cartResult =
          await globals.client.value.mutate(getProductsInCartOptions);

      if (cartResult.hasException) {
        setState(() {
          _dataFetched = true;
          _products = [];
        });
      }

      products = HelperFunctions.deserializeListData(cartResult);

      double newCartTotal = 0;

      for (Map<String, dynamic> product in products) {
        newCartTotal += double.parse(product['productPrice']['price']) *
            product['quantity'];
      }

      setState(() {
        _cartTotal = newCartTotal;
        _dataFetched = true;
        _products = products;
      });
    }
  }

  List<Widget> _buildCartProducts(List<Map<String, dynamic>> products) {
    Map<String, dynamic> cartProducts = {};

    for (Map<String, dynamic> product in products) {
      if (!cartProducts.containsKey(product['productPrice']['id'])) {
        cartProducts.putIfAbsent(
            product['productPrice']['id'],
            () => {
                  'locked': product['locked'],
                  'quantity': product['quantity'],
                  'productPrice': product['productPrice'],
                });
      } else {
        cartProducts[product['productPrice']['id']]['quantity'] +=
            product['quantity'];
      }
    }

    return cartProducts
        .map((id, productData) => MapEntry(
            id,
            CartProduct(
              isLocked: productData['locked'],
              quantity: productData['quantity'],
              product: productData['productPrice'],
              bottomBorder: true,
              addPriceToTotal: addPriceToTotal,
            )))
        .values
        .toList();
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
      appBar: MainPageAppBar(
        text: kCartText,
        actions: [
          Container(
            decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.7),
                borderRadius: const BorderRadius.all(Radius.circular(10))),
            height: 50,
            width: 100,
            margin: const EdgeInsets.all(5),
            padding: const EdgeInsets.all(5),
            alignment: Alignment.center,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                const Icon(
                  Icons.shopping_cart,
                  color: kPrimaryColor,
                ),
                Text("${_cartTotal.toStringAsFixed(2)} €",
                    style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                        color: kPrimaryColor))
              ],
            ),
          )
        ],
      ),
      floatingActionButton: ExpandableFab(
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
                              labelStyle:
                                  TextStyle(overflow: TextOverflow.ellipsis),
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
                                              const CartPage()));
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
                                labelStyle:
                                    TextStyle(overflow: TextOverflow.ellipsis),
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
                              paddingContainer:
                                  const EdgeInsets.fromLTRB(75, 25, 75, 10),
                              text: "CREAR LISTA",
                              action: () {
                                final isvalid =
                                    _formkey.currentState!.validate();
                                if (isvalid) {
                                  _formkey.currentState!.save();
                                  _createList(listName).then((edited) {
                                    Navigator.of(context).pop();
                                    if (edited) {
                                      Navigator.of(context).pushReplacement(
                                        MaterialPageRoute(
                                            builder: (context) =>
                                                const MainScreen(
                                                  firstScreen: Screens.list,
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
      body: FutureBuilder(
          future: _getProductsInCart(),
          builder: (context, products) {
            if (_products != null) {
              if (_products!.isEmpty) {
                return const Center(
                  child: Text('No tienes productos en el carrito'),
                );
              } else {
                return ListView(
                  children: _buildCartProducts(_products!),
                );
              }
            } else {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }
          }),
      bottomNavigationBar: KununuaNavBar(
        screen: Screens.cart,
        currentScreenCallback: (Screens screen) {
          Navigator.of(context).pushReplacement(MaterialPageRoute(
              builder: (context) => MainScreen(
                    firstScreen: screen,
                  )));
        },
      ),
    );
  }
}
