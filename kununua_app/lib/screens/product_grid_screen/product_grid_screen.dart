import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/app_bars/common_app_bar.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_cell.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/widgets/kununua_grid.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class ProductGridScreen extends StatelessWidget {
  final String category;

  const ProductGridScreen({
    super.key,
    required this.category,
  });

  Future<List<Map<String, dynamic>>> _getProductsByCategory() async {

    final MutationOptions getProducts = MutationOptions(
      document: gql(getProductsByCategory),
      variables: <String, dynamic>{
        'categoryName': category,
      },
    );

    final productsResult = await globals.client.value.mutate(getProducts);

    var productsList = HelperFunctions.deserializeListData(productsResult);

    return productsList;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CommonAppBar(
        text: category,
      ),
      body: Container(
        color: kBackgroundColor,
        child: FutureBuilder(
          future: _getProductsByCategory(),
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            if (snapshot.hasData) {
              return KununuaGrid(
                      scrollable: true,
                      gridMargin: const EdgeInsets.fromLTRB(20, 10, 20, 10),
                      mainAxisSpacing: 10,
                      crossAxisCount: 2,
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children:
                          snapshot.data.map<Widget>((product) => ProductGridCell(
                                id: int.parse(product['id']),
                                image: product['imageEncoded'],
                                title: product['name'],
                                price: product['price'],
                                offerPrice: product['offerPrice'] ?? '',
                                unitPrice: product['unitPrice'],
                                weightUnit: product['weightUnit'] ?? '',
                                currency: product['supermarket']['country']['currency']['symbol'] ?? 
                                            product['supermarket']['country']['currency']['code'],
                              )).toList()
                      );
            } else {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }
          },
        ),
      ),
    );
  }
}
