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

  @override
  Widget build(BuildContext context) {
    return Container(
              margin: const EdgeInsets.only(top: 20, bottom: 20),
              height: 120,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: const [
                  Image(
                    image: AssetImage("assets/icons/without-lactose-icon.png"),
                    height: 50,
                    width: 50,  
                  ),
                  Image(
                    image: AssetImage("assets/icons/eco-friendly-icon.png"),
                    height: 50,
                    width: 50,  
                  ),
                  Image(
                    image: AssetImage("assets/icons/gluten-free-icon.png"),
                    height: 50,
                    width: 50,  
                  ),
                  Image(
                    image: AssetImage("assets/icons/vegan-icon.png"),
                    height: 50,
                    width: 50,  
                  ),
                  Image(
                    image: AssetImage("assets/icons/without-sugar-icon.png"),
                    height: 50,
                    width: 50,  
                  ),
                  Image(
                    image: AssetImage("assets/icons/country-icon.png"),
                    height: 50,
                    width: 50,  
                  ),
                ],
              ),
            );
  }
}