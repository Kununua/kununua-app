import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';

class ProductNameRow extends StatelessWidget {
  
  final String productName;
  
  const ProductNameRow({
    super.key,
    required this.productName,  
  });

  @override
  Widget build(BuildContext context) {
    return Container(
            margin: const EdgeInsets.only(bottom: 20),
            child: Text(
              productName.capitalizeFirstOfEach(),
              style: const TextStyle(
                color: Colors.black,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
          );
  }
}

class PriceRow extends StatelessWidget {

  final String supermarket;
  final String price;
  final String? offerPrice;

  const PriceRow({
    super.key,
    required this.supermarket,
    required this.price,
    this.offerPrice,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Row(
                children: [
                  const Icon(
                    Ionicons.location,
                    size: 18,
                    color: kPrimaryColor,
                  ),
                  Text(
                    " ${supermarket.capitalizeFirstOfEach()}",
                    style: const TextStyle(
                      color: kPrimaryColor,
                      fontSize: 18,
                    ),
                  ),
                ],
              ),
              offerPrice == null ?
                Text(
                  price,
                  style: const TextStyle(
                    color: kPrimaryColor,
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                )
                :
                Row(
                  children: [
                    Text(
                      "$price  ",
                      style: const TextStyle(
                        color: Color.fromARGB(255, 103, 102, 102),
                        fontSize: 18,
                        fontWeight: FontWeight.normal,
                        decoration: TextDecoration.lineThrough,
                      ),
                    ),
                    Text(
                      "${offerPrice}",
                      style: const TextStyle(
                        color: kPrimaryColor,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
            ],
          );
                      
  }
}

class FlagsRow extends StatelessWidget {

  final bool isVegetarian;
  final bool isGlutenFree;
  final bool isFreezed;
  final bool isFromCountry;
  final bool isEco;
  final bool isWithoutSugar;
  final bool isWithoutLactose;

  const FlagsRow({
    super.key,
    required this.isVegetarian,
    required this.isGlutenFree,
    required this.isFreezed,
    required this.isFromCountry,
    required this.isEco,
    required this.isWithoutSugar,
    required this.isWithoutLactose,
  });

  List<Image> getFlags() {
    final flagDirs = [
      "assets/icons/vegan-icon.png",
      "assets/icons/gluten-free-icon.png",
      "assets/icons/freezed-icon.png",
      "assets/icons/country-icon.png",
      "assets/icons/eco-friendly-icon.png",
      "assets/icons/without-sugar-icon.png",
      "assets/icons/without-lactose-icon.png",
    ];

    final flagValues = [
      isVegetarian,
      isGlutenFree,
      isFreezed,
      isFromCountry,
      isEco,
      isWithoutSugar,
      isWithoutLactose,
    ];

    final flags = <Image>[];

    for (var i = 0; i < flagDirs.length; i++) {
      if (flagValues[i]) {
        flags.add(Image(
          image: AssetImage(flagDirs[i]),
          width: 50,
          height: 50,
        ));
      }
    }

    return flags;
  }

  @override
  Widget build(BuildContext context) {

    return Container(
              margin: const EdgeInsets.only(top: 20, bottom: 20),
              height: 120,
              child: GridView.count(
                crossAxisCount: 4,
                mainAxisSpacing: 10,
                crossAxisSpacing: 20,
                childAspectRatio: 1/1,
                children: getFlags(),
              ),
            );
  }
}