import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/widgets/kununua_confirm.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';

class CartProduct extends StatefulWidget {
  
  final Map<String, dynamic> product;
  final int quantity;
  final bool topBorder;
  final bool bottomBorder;

  const CartProduct({
    super.key,
    required this.product,
    required this.quantity,
    this.topBorder = false,
    this.bottomBorder = false,
  });

  @override
  State<CartProduct> createState() => _CartProductState();
}

class _CartProductState extends State<CartProduct> {

  late int amount;

  @override
  void initState() {
    super.initState();
    amount = widget.quantity;
  }

  Future<bool> editCartEntryRequest(int productId, int amount) async {
    Map<String, dynamic> product = {};

    final MutationOptions editCartEntryOptions = MutationOptions(
      document: gql(editCartEntry),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
        'productId': productId,
        'amount': amount,
      },
    );

    final entryResult = await globals.client.value.mutate(editCartEntryOptions);

    return !entryResult.hasException;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(left: 10),
      height: 125,
      decoration: BoxDecoration(
        border: Border(
          top: BorderSide(
            color: widget.topBorder ? Colors.grey : Colors.transparent,
            width: 2,
          ),
          bottom: BorderSide(
            color: widget.bottomBorder ? Colors.grey : Colors.transparent,
            width: 2,
          ),
        ),
      ),
      child: Row(
        children: [
          Image(
            image: widget.product['image'],
            width: 100,
            height: 100,
            fit: BoxFit.cover
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(10),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    (widget.product["name"] as String)
                        .title(),
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    widget.product["supermarket"]['name'],
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "${widget.product["price"]} €",
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Row(
                        children: [
                          IconButton(
                            onPressed: () {
                              if(amount - 1 == 0){
                                showDialogWidget(
                                  context,
                                  KununuaConfirm(
                                    title: "Eliminar producto",
                                    text: "¿Está seguro de que desea eliminar este producto del carrito?",
                                    onConfirm: () {
                                      Navigator.of(context).pop();
                                      editCartEntryRequest(int.parse(widget.product["id"]), 0).then((edited){
                                        if(edited){
                                          Navigator.of(context).pushReplacement(
                                            MaterialPageRoute(
                                              builder: (context) => const MainScreen(
                                                firstScreen: Screens.cart,
                                              )
                                            ),
                                          );
                                        }else{
                                          ScaffoldMessenger.of(context).showSnackBar(
                                            const SnackBar(
                                              content: Text("No se ha podido editar la entrada del carrito. Por favor, inténtelo de nuevo."),
                                            ),
                                          );
                                        }
                                      });
                                    },
                                    onCancel: () {
                                      Navigator.of(context).pop();
                                    },
                                  ),
                                );
                              }else{
                                editCartEntryRequest(int.parse(widget.product["id"]), amount-1).then((edited){
                                if(edited){
                                  setState(() {
                                    if (amount > 1){
                                      amount--;
                                    }
                                  });
                                }else{
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text("No se ha podido editar la entrada del carrito. Por favor, inténtelo de nuevo."),
                                    ),
                                  );
                                }
                              });
                              }
                            },
                            icon: const Icon(Icons.remove),
                          ),
                          Text(
                            amount.toString(),
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          IconButton(
                            onPressed: () {
                              editCartEntryRequest(int.parse(widget.product["id"]), amount+1).then((edited){
                                if(edited){
                                  setState(() {
                                    amount++;
                                  });
                                }else{
                                  ScaffoldMessenger.of(context).showSnackBar(
                                    const SnackBar(
                                      content: Text("No se ha podido editar la entrada del carrito. Por favor, inténtelo de nuevo."),
                                    ),
                                  );
                                }
                              });
                            },
                            icon: const Icon(Icons.add),
                          ),
                        ],
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}