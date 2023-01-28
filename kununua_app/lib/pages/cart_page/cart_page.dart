import 'package:flutter/material.dart';
import 'package:kununua_app/pages/cart_page/components/cart_product.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/requests.dart';

class CartPage extends StatelessWidget {
  const CartPage({super.key});

  Future<List<Map<String, dynamic>>> _getProductsInCart() async{

    List<Map<String, dynamic>> products = [];

    final MutationOptions getProductsInCartOptions = MutationOptions(
      document: gql(getProductsInCart),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
      },
    );

    final cartResult = await globals.client.value.mutate(getProductsInCartOptions);

    if (cartResult.hasException) {
      return [];
    }

    products = HelperFunctions.deserializeListData(cartResult);

    return products;

  }

  List<Widget> _buildCartProducts(List<Map<String, dynamic>> products) {

    List<Widget> cartProducts = [];

    for (Map<String, dynamic> product in products) {
      //print(product);
      cartProducts.add(CartProduct(
        quantity: product['quantity'],
        product: product['product']
      ));
    }

    return cartProducts;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
      future: _getProductsInCart(),
      builder: (context, products){
        if(products.hasData){
          return ListView(
            children: _buildCartProducts(products.data!),
          );
        }else{
          return const Center(
            child: CircularProgressIndicator(),
          );
        }
      }
    );
  }
}