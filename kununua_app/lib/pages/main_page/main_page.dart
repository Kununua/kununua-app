import 'package:flutter/material.dart';
import 'package:kununua_app/pages/main_page/components/main_page_category_row/main_page_category_row.dart';
import 'package:kununua_app/pages/main_page/components/carousel.dart';
import 'package:kununua_app/pages/main_page/components/main_page_row/main_page_cell.dart';
import 'package:kununua_app/pages/main_page/components/main_page_row/main_page_row.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:graphql_flutter/graphql_flutter.dart';


class MainPage extends StatelessWidget {
  const MainPage({super.key});

  Future<List<Widget>> _getOfferProducts() async{

    List<Widget> offerProducts = [];

    final QueryOptions getOfferProductsOptions = QueryOptions(
      document: gql(getOfferProducts),
    );

    final offerProductsResult = await globals.client.value.query(getOfferProductsOptions);

    if (offerProductsResult.hasException) {
      return [];
    }

    final offerProductsData = HelperFunctions.deserializeListData(offerProductsResult);

    for (Map<String, dynamic> product in offerProductsData) {
      offerProducts.add(
        MainPageCell(
          product: product,
          bgImage: product['image'],
        )
      );
    }

    return offerProducts;

  }

  Future<List<Widget>> _getPacks() async {
    List<Widget> packsProducts = [];

    final QueryOptions getPackProductsOptions = QueryOptions(
      document: gql(getPacks),
    );

    final packProductsResult =
        await globals.client.value.query(getPackProductsOptions);

    if (packProductsResult.hasException) {
      return [];
    }

    final packProductsData =
        HelperFunctions.deserializeListData(packProductsResult);

    for (Map<String, dynamic> product in packProductsData) {
      packsProducts.add(MainPageCell(
        product: product,
        bgImage: product['image'],
      ));
    }

    return packsProducts;
  }

  @override
  Widget build(BuildContext context) {

    final screenSize = MediaQuery.of(context).size;

    return Container(
        height: screenSize.height,
        width: screenSize.width,
        color: kBackgroundColor,
        child: SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.max,
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const MainCarousel(),
              const MainPageCategoryRow(),
              FutureBuilder(
                future: _getOfferProducts(),
                builder: (context, products){
                  if(products.hasData){
                    if ((products.data ?? []).isEmpty){
                      return const Padding(
                          padding: EdgeInsets.only(top: 10),
                          child: Center(
                        child: Text('No hay productos en oferta'),
                          ));
                    }else{
                      return MainPageRow(rowName: 'En oferta', cells: products.data!);
                    }
                  }else{
                    return const MainPageRow(rowName: 'En oferta', loading: true);
                  }
                }
              ),
            FutureBuilder(
                future: _getPacks(),
                builder: (context, products) {
                  if (products.hasData) {
                    if ((products.data ?? []).isEmpty) {
                      return const Padding(
                          padding: EdgeInsets.only(top: 10),
                          child: Center(
                            child: Text('No hay packs disponibles'),
                          ));
                    } else {
                      return MainPageRow(
                          rowName: 'Packs', cells: products.data!);
                    }
                  } else {
                    return const MainPageRow(rowName: 'Packs', loading: true);
                  }
                }),
              const MainPageRow(rowName: 'Volver a comprar'),
              const MainPageRow(rowName: 'Productos más vendidos'),
            ],
          ),
        ),
      );
  }
}