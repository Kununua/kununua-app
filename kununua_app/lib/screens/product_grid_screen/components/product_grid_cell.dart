import 'package:animations/animations.dart';
import 'package:flutter/material.dart';
import 'package:kununua_app/screens/product_details_screen/product_details_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';

class ProductGridCell extends StatelessWidget {
  final int id;
  final ImageProvider image;
  final String title;
  final String price;
  final String offerPrice;
  final String unitPrice;
  final String weightUnit;
  final String currency;

  const ProductGridCell(
      {super.key,
      required this.id,
      required this.image,
      required this.title,
      required this.price,
      this.offerPrice = "",
      required this.unitPrice,
      required this.weightUnit,
      required this.currency});

  @override
  Widget build(BuildContext context) {
    return OpenContainer(
      transitionType: ContainerTransitionType.fade,
      transitionDuration: const Duration(milliseconds: 500),
      closedColor: kBackgroundColor,
      closedElevation: 0,
      clipBehavior: Clip.none,
      closedBuilder: (context, openDetails){
        return Container(
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
          ),
          child:
              Column(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
            SizedBox(
                width: 150,
                height: 100,
                child: Image(
                  image: image,
                  fit: BoxFit.contain,
                )),
            Padding(
              padding: const EdgeInsets.only(top: 10),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly, 
                children: [
                  offerPrice != ""
                      ? Row(
                        children: [
                          Text(price + currency,
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            fontSize: 12,
                            decoration: TextDecoration.lineThrough,
                            color: Colors.grey,
                          )),
                          Text(
                            offerPrice + currency,
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          )
                        ],
                      )
                      : 
                      Text(
                          price + currency,
                          textAlign: TextAlign.center,
                          style: const TextStyle(
                            fontSize: 12,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                ]
              ),
            ),
            Text("($unitPrice)",
                style: const TextStyle(
                  fontSize: 9,
                )),
            Text(title.limitCharacters(25).capitalizeFirstOfEach(),
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.bold,
                )),
            Text(weightUnit,
                style: const TextStyle(
                  fontSize: 9,
                ))
          ]));
      },
      openBuilder: (context, action) {
          return ProductDetails(productId: id,);
      },
      onClosed: (_) {},
    );
  }
}
