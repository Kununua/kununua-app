import 'dart:ffi';

import 'package:flutter/material.dart';

class ProductGridCell extends StatelessWidget {
  final Int id;
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

  String _checkTitleLength(String title) {
    if (title.length > 39) {
      return "${title.substring(0, 36)}...";
    } else {
      return title;
    }
  }

  @override
  Widget build(BuildContext context) {
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
          Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [
            offerPrice != ""
                ? Text(price + currency,
                    style: const TextStyle(
                      fontSize: 12,
                      decoration: TextDecoration.lineThrough,
                      color: Colors.grey,
                    ))
                : Container(),
            offerPrice != ""
                ? Text(
                    offerPrice + currency,
                    style: const TextStyle(fontSize: 12),
                  )
                : Text(
                    price + currency,
                    style: const TextStyle(fontSize: 12),
                  ),
          ]),
          Text("($unitPrice)",
              style: const TextStyle(
                fontSize: 9,
              )),
          Text(_checkTitleLength(title),
              style: const TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.bold,
              )),
          Text(weightUnit,
              style: const TextStyle(
                fontSize: 9,
              ))
        ]));
  }
}
