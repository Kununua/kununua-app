import 'package:animations/animations.dart';
import 'package:flutter/material.dart';
import 'package:carousel_slider/carousel_slider.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

import '../../../screens/product_grid_screen/product_grid_screen.dart';
import '../../../utils/constants.dart';

class MainCarousel extends StatelessWidget {
  const MainCarousel({super.key});

  Future<List<Map<String, dynamic>>> _getSupermarkets() async {
    final QueryOptions getSupermarketsQuery = QueryOptions(
      document: gql(getSupermarkets),
    );

    final productsResult =
        await globals.client.value.query(getSupermarketsQuery);

    if (productsResult.hasException) {
      return [];
    }

    List<Map<String, dynamic>> resultList =
        HelperFunctions.deserializeListData(productsResult);

    return resultList;
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.fromLTRB(0, 20, 0, 20),
        child: FutureBuilder(
          future: _getSupermarkets(),
          builder: (context, snapshot) {
            if (snapshot.hasData) {
              List<Map<String, dynamic>> supermarkets = snapshot.data!;

              return CarouselSlider(
                options: CarouselOptions(
                  autoPlay: true,
                  enlargeCenterPage: true,
                  aspectRatio: 16 / 9,
                  height: 200.0,
                ),
                items: supermarkets.map((supermarket) {
                  return Builder(
                    builder: (BuildContext context) {
                      return OpenContainer(
                        transitionType: ContainerTransitionType.fade,
                        transitionDuration: const Duration(milliseconds: 500),
                        closedColor: kBackgroundColor,
                        closedElevation: 0,
                        clipBehavior: Clip.none,
                        closedBuilder: (context, openContainer) {
                          return Container(
                            width: MediaQuery.of(context).size.width,
                            margin: const EdgeInsets.symmetric(horizontal: 5.0),
                            decoration: BoxDecoration(
                                borderRadius: const BorderRadius.all(
                                    Radius.circular(20.0)),
                                border: Border.all(
                                    color: kPrimaryColor, width: 2.0),
                                image: DecorationImage(
                                  image: supermarket['banner'],
                                  fit: BoxFit.fill,
                                )),
                          );
                        },
                        openBuilder: (context, action) {
                          return ProductGridScreen(
                              supermarketId: int.parse(supermarket['id']),
                              supermarketName: supermarket['name'],
                              isSupermarket: true);
                        },
                        onClosed: (_) {},
                      );
                    },
                  );
                }).toList(),
              );
            } else {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }
          },
        ));
  }
}
