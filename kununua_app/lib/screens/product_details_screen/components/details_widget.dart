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
              leading: Platform.isIOS ? const Icon(Icons.arrow_back_ios) : const Icon(Icons.arrow_back),
              title: Container(),
              appBarColor: kPrimaryColor,
              alwaysShowTitle: false,
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
                      ProductNameRow(productName: product['name']),
                      PriceRow(
                        supermarket: product['supermarket']['name'], 
                        price: "${product['price']} ${product['supermarket']['country']['currency']['symbol']}",
                        offerPrice: product['offerPrice'] != null ? "${product['offerPrice']} ${product['supermarket']['country']['currency']['symbol']}" : null,
                      ),
                      FlagsRow(
                        isVegetarian: true,//product['isVegetarian'],
                        isGlutenFree: true,//product['isGlutenFree'],
                        isEco: true,//product['isEco'],
                        isFreezed: true,//product['isFreezed'],
                        isFromCountry: true,//product['isFromCountry'],
                        isWithoutLactose: true,//product['isWithoutLactose'],
                        isWithoutSugar: true,//product['isWithoutSugar'],
                      ),
                    ]
                  ),
                ),
              ]
            );
  }
}