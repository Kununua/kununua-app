import 'package:flutter/material.dart';
import 'package:kununua_app/pages/list_page/components/list_product.dart';
import 'package:kununua_app/utils/constants.dart';

class ListExtendedView extends StatelessWidget {
  const ListExtendedView(
      {super.key, required this.title, required this.products});

  final String title;
  final List<dynamic> products;

  List<Widget> _buildLists() {
    Map<String, dynamic> listProducts = {};

    for (Map<String, dynamic> product in products) {

      if (!listProducts.containsKey(product['productPrice']['id'])){

        listProducts.putIfAbsent(product['productPrice']['id'], () => {
          'quantity': product['quantity'],
          'productPrice': product['productPrice']
        });

      }else{
        listProducts[product['productPrice']['id']]['quantity'] += product['quantity'];
      }
    }

    return listProducts.map((id, productData) => MapEntry(id, ListProduct(
          quantity: productData['quantity'],
          product: productData['productPrice']
        )) ).values.toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(title),
          titleTextStyle: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.w300,
              overflow: TextOverflow.ellipsis,
              color: Colors.white),
          backgroundColor: kPrimaryColor,
        ),
        body: SizedBox(
          height: double.infinity,
          width: double.infinity,
          child: ListView(
            children: _buildLists(),
          ),
        ));
  }
}
