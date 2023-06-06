import 'dart:io';
import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/screens/product_details_screen/components/details_header.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/screens/product_details_screen/components/draggable_home.dart';
import 'package:kununua_app/screens/product_details_screen/components/details_library.dart';

class DetailsWidget extends StatefulWidget {
  
  final Map<String, dynamic> product;
  
  const DetailsWidget({
    super.key,
    required this.product,
  });

  @override
  State<DetailsWidget> createState() => _DetailsWidgetState();
}

class _DetailsWidgetState extends State<DetailsWidget> {

  int selectedPriceId = 0;

  void updateSelectedPriceId(int selectedPriceIdParam) {
    setState(() {
      selectedPriceId = selectedPriceIdParam;
    });
  }

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
              headerWidget: DetailsHeader(productImage: widget.product['image'],),
              // expandedBody: const CameraPreview(),
              body: [
                Padding(
                  padding: const EdgeInsets.only(left: 20, right: 20),
                  child: Column(
                    children: [
                      ProductNameRow(
                        productName: widget.product['name']
                      ),
                      RatingRow(
                        rating: 4.5
                      ),
                      PriceRow(
                        productPriceSet: widget.product['priceSet'],
                        selectedPriceId: selectedPriceId,
                        priceIdUpdater: updateSelectedPriceId,
                      ),
                      FlagsRow(
                        isVegetarian: widget.product['isVegetarian'] ?? false,
                        isGlutenFree: widget.product['isGlutenFree'] ?? false,
                        isEco: widget.product['isEco'] ?? false,
                        isFreezed: widget.product['isFreezed'] ?? false,
                        isFromCountry: widget.product['isFromCountry'] ?? false,
                        isWithoutLactose: widget.product['isWithoutLactose'] ?? false,
                        isWithoutSugar: widget.product['isWithoutSugar'] ?? false,
                      ),
                      OpinionsRow(
                        productId: widget.product['id'],
                      ),
                    ]
                  ),
                ),
              ],
              bottomNavigationBar: AddToCart(
                  priceId: selectedPriceId,
                ),
            );
  }
}