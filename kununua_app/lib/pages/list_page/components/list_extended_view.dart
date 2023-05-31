import 'package:flutter/material.dart';
import 'package:kununua_app/pages/list_page/components/list_product.dart';
import 'package:kununua_app/utils/constants.dart';

class ListExtendedView extends StatelessWidget {
  const ListExtendedView(
      {super.key, required this.title, required this.products});

  final String title;
  final List<Object?> products;

  List<Widget> _buildLists() {
    List<Widget> listProducts = [];

    for (Object? list in products) {
      list = list as Map<String, dynamic>;
      listProducts.add(ListProduct(
          product: list['productPrice'], quantity: list['quantity']));
    }

    return listProducts;
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
