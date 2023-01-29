import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/widgets/kununua_grid.dart';
import 'package:flutter_rating_bar/flutter_rating_bar.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';

class ProductNameRow extends StatelessWidget {
  
  final String productName;
  
  const ProductNameRow({
    super.key,
    required this.productName,  
  });

  @override
  Widget build(BuildContext context) {
    return Container(
            margin: const EdgeInsets.only(bottom: 10),
            child: Text(
              productName.capitalizeFirstOfEach(),
              textAlign: TextAlign.center,
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

  List<Image> _getFlags() {
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

    for (var i = 0; i < flagValues.length; i++) {
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
    return KununuaGrid(
            crossAxisCount: 4,
            gridMargin: const EdgeInsets.only(top: 20, bottom: 20),
            children: _getFlags(),
          );
  }
}

class RatingRow extends StatelessWidget {

  final double rating;

  const RatingRow({
    super.key,
    required this.rating,  
  });

  @override
  Widget build(BuildContext context) {

    if (rating < 0 || rating > 5) {
      throw Exception("Rating must be between 0 and 5");
    }

    return Container(
            margin: const EdgeInsets.only(bottom: 10),
            child: RatingBar.builder(
                    initialRating: rating,
                    minRating: 1,
                    direction: Axis.horizontal,
                    allowHalfRating: true,
                    ignoreGestures: true,
                    itemCount: 5,
                    itemSize: 30,
                    itemPadding: const EdgeInsets.symmetric(horizontal: 2.0),
                    itemBuilder: (context, _) => const Icon(
                      Icons.star,
                      color: Colors.amber,
                    ),
                    onRatingUpdate: (rating) {},
                  ),
            );
  }
}

class AddToCart extends StatefulWidget {

  final int productId;

  const AddToCart({
    super.key,
    required this.productId,
  });

  @override
  State<AddToCart> createState() => _AddToCartState();
}

class _AddToCartState extends State<AddToCart> {

  int amount = 1;

  Future<bool> addProductToCart() async {

    final MutationOptions addEntryToCartOptions = MutationOptions(
      document: gql(addToCart),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
        'productId': widget.productId,
        'amount': amount,
      },
    );

    final productResult = await globals.client.value.mutate(addEntryToCartOptions);

    return !productResult.hasException;

  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(left: 20, right: 20, bottom: 20),
      child: SizedBox(
        width: MediaQuery.of(context).size.width - 40,
        height: kAddToCartButtonHeight,
        child: ElevatedButton(
          onPressed: (){
            addProductToCart().then((added){
              if(added){
                Navigator.of(context).pushAndRemoveUntil(
                  MaterialPageRoute(
                    builder: (context) => const MainScreen(
                      firstScreen: Screens.cart,
                    ),
                  ),
                  (route) => false,
                );
              }else{
                ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(
                    content: Text("No se ha podido añadir el producto al carrito"),
                  ),
                );
              }
              }
            );
          }, 
          style: ButtonStyle(
            backgroundColor: MaterialStateProperty.all<Color>(kPrimaryColor),
            shape: MaterialStateProperty.all<RoundedRectangleBorder>(
              RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(18.0),
              ),
            ),
          ),
          child: SizedBox(
            width: double.infinity,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Flexible(
                  flex: 2,
                  child: SizedBox(
                    width: double.infinity,
                    child: Text(
                      "AÑADIR AL CARRITO",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                ),
                Container(
                  alignment: Alignment.centerRight,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      IconButton(
                        onPressed: (){
                          setState(() {
                            if (amount > 1) {
                              amount--;
                            }
                          });
                        }, 
                        icon: const Icon(
                          Ionicons.remove,
                          color: Colors.white,
                          size: 30,
                        ),
                      ),
                      Text(
                        "$amount",
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      IconButton(
                        onPressed: (){
                          setState(() {
                            amount++;
                          });
                        }, 
                        icon: const Icon(
                          Ionicons.add,
                          color: Colors.white,
                          size: 30,
                        ),
                      ),
                    ],
                  ),
                ),
              ]
            ),
          ),
        ),
      ),
    );
  }
}