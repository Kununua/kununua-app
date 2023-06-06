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
        productName.title(),
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
  final List<dynamic> productPriceSet;
  final int selectedPriceId;
  final Function priceIdUpdater;

  const PriceRow({
    super.key,
    required this.productPriceSet,
    required this.selectedPriceId,
    required this.priceIdUpdater,
  });

  List<Widget> getSingleProductCards() {
    List<Widget> result = [];

    for (dynamic price in productPriceSet) {
      result.add(GestureDetector(
        onTap: () {
          priceIdUpdater(int.parse(price['id']));
        },
        child: Container(
            width: 150,
            height: 200,
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              boxShadow: const [
                BoxShadow(
                  offset: Offset(0, 17),
                  blurRadius: 10,
                  spreadRadius: -13,
                  color: Colors.black,
                ),
              ],
              border: selectedPriceId == int.parse(price['id'])
                  ? Border.all(color: kPrimaryColor, width: 2)
                  : null,
            ),
            child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  SizedBox(
                      width: 150,
                      height: 100,
                      child: Image(
                        image: price['supermarket']['image'],
                        fit: BoxFit.contain,
                      )),
                  Padding(
                    padding: const EdgeInsets.only(top: 10),
                    child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Text(
                            price['price'] +
                                price['supermarket']['country']['currency']
                                    ['symbol'],
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ]),
                  ),
                  // Text("($unitPrice)",
                  //     style: const TextStyle(
                  //       fontSize: 9,
                  //     )),
                  Text((price['supermarket']['name'] as String).title(),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      textAlign: TextAlign.center,
                      style: const TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.bold,
                      )),
                  Text(price['weight'],
                      style: const TextStyle(
                        fontSize: 9,
                      ))
                ])),
      ));
    }

    return result;
  }

  @override
  Widget build(BuildContext context) {
    return KununuaGrid(
      crossAxisCount: 2,
      gridMargin: const EdgeInsets.only(top: 20, bottom: 20),
      children: getSingleProductCards(),
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
  final bool allowEdit;
  final bool halfRating;
  void Function(double)? onChange;

  RatingRow({
    super.key,
    required this.rating,
    this.allowEdit = false,
    this.halfRating = true,
    this.onChange,
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
        allowHalfRating: halfRating,
        ignoreGestures: !allowEdit,
        itemCount: 5,
        itemSize: 30,
        itemPadding: const EdgeInsets.symmetric(horizontal: 2.0),
        itemBuilder: (context, _) => const Icon(
          Icons.star,
          color: Colors.amber,
        ),
        onRatingUpdate: onChange ?? (double value) {},
      ),
    );
  }
}

class AddToCart extends StatefulWidget {
  final int priceId;

  const AddToCart({
    super.key,
    required this.priceId,
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
        'priceId': widget.priceId,
        'amount': amount,
      },
    );

    final productResult =
        await globals.client.value.mutate(addEntryToCartOptions);

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
          onPressed: widget.priceId == 0
              ? null
              : () {
                  addProductToCart().then((added) {
                    if (added) {
                      Navigator.of(context).pushAndRemoveUntil(
                        MaterialPageRoute(
                          builder: (context) => const MainScreen(
                            firstScreen: Screens.cart,
                          ),
                        ),
                        (route) => false,
                      );
                    } else {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text(
                              "No se ha podido añadir el producto al carrito"),
                        ),
                      );
                    }
                  });
                },
          style: ButtonStyle(
            backgroundColor: widget.priceId != 0
                ? MaterialStateProperty.all<Color>(kPrimaryColor)
                : MaterialStateProperty.all<Color>(
                    const Color.fromARGB(255, 161, 179, 188)),
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
                          onPressed: () {
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
                          onPressed: () {
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
                ]),
          ),
        ),
      ),
    );
  }
}

class OpinionsRow extends StatefulWidget {
  final String productId;

  const OpinionsRow({
    super.key,
    required this.productId,
  });

  @override
  State<OpinionsRow> createState() => _OpinionsRowState();
}

class _OpinionsRowState extends State<OpinionsRow> {
  double ratingValue = 0;

  Future<void> addOpinion(BuildContext context) async {
    final MutationOptions addOpinionOptions = MutationOptions(
      document: gql(addOpinionRequest),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
        'productId': int.parse(widget.productId),
        'rating': ratingValue,
      },
    );

    final productResult = await globals.client.value.mutate(addOpinionOptions);

    if (context.mounted) {
      if (productResult.hasException) {
        if (productResult.exception
            .toString()
            .contains("You have already rated this product")) {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("Ya has valorado este producto"),
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            const SnackBar(
              content: Text("No se ha podido añadir la opinión"),
            ),
          );
        }
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text("Opinión añadida correctamente"),
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      mainAxisSize: MainAxisSize.max,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        const Text("¿Qué opinas sobre este producto?",
            style: TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold,
            )),
        Container(
          margin: const EdgeInsets.only(top: 10),
          child: RatingRow(
            rating: 0,
            halfRating: false,
            allowEdit: true,
            onChange: (rating) {
              setState(() {
                ratingValue = rating;
              });
            },
          ),
        ),
        GestureDetector(
          onTap: () {
            if (ratingValue != 0) {
              addOpinion(context);
            } else {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text(
                      "Debes puntuar el producto para publicar la valoración"),
                ),
              );
            }
          },
          child: Container(
            margin: const EdgeInsets.only(top: 10, bottom: 50),
            child: const Text(
              "OPINAR",
              style: TextStyle(
                  color: kPrimaryColor,
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  decoration: TextDecoration.underline,
                  ),
            ),
          ),
        ),
      ],
    );
  }
}
