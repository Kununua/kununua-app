import 'dart:io';
import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/screens/product_details_screen/components/details_header.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/screens/product_details_screen/components/draggable_home.dart';
import 'package:kununua_app/screens/product_details_screen/components/details_library.dart';

class DetailsWidget extends StatelessWidget {
  
  final Map<String, dynamic> product;
  
  const DetailsWidget({
    super.key,
    required this.product,
  });

  @override
  Widget build(BuildContext context) {

    return DraggableHome(
              title: Container(),
              appBarColor: kPrimaryColor,
              backgroundColor: const Color.fromARGB(255, 231, 231, 231),
              shadowBorder: true,
              curvedBodyRadius: 40,
              // fullyStretchable: true,
              alwaysShowLeadingAndAction: true,
              headerWidget: DetailsHeader(productImage: product['image'],),
              // expandedBody: const CameraPreview(),
              body: [
                Padding(
                  padding: const EdgeInsets.only(left: 20, right: 20),
                  child: Column(
                    children: [
                      ProductNameRow(
                        productName: product['name']
                      ),
                      const RatingRow(
                        rating: 4.5
                      ),
                      PriceRow(
                        supermarket: product['priceSet'][0]['supermarket']['name'], 
                        price: "${product['priceSet'][0]['price']} ${product['priceSet'][0]['supermarket']['country']['currency']['symbol']}",
                        offerPrice: product['priceSet'][0]['amount'] != null ? "${product['priceSet'][0]['price']} ${product['priceSet'][0]['supermarket']['country']['currency']['symbol']}" : null,
                      ),
                      FlagsRow(
                        isVegetarian: product['isVegetarian'] ?? false,
                        isGlutenFree: product['isGlutenFree'] ?? false,
                        isEco: product['isEco'] ?? false,
                        isFreezed: product['isFreezed'] ?? false,
                        isFromCountry: product['isFromCountry'] ?? false,
                        isWithoutLactose: product['isWithoutLactose'] ?? false,
                        isWithoutSugar: product['isWithoutSugar'] ?? false,
                      ),
                    ]
                  ),
                ),
              ],
              bottomNavigationBar: AddToCart(
                  productId: int.parse(product['id']),
                ),
            );
  }
}