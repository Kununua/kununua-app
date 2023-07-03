import 'package:animations/animations.dart';
import 'package:flutter/material.dart';
import 'package:kununua_app/screens/product_details_screen/product_details_screen.dart';
import 'package:kununua_app/utils/constants.dart';

class MainPageCell extends StatelessWidget {
  
  final Map<String, dynamic> product;
  final ImageProvider bgImage;
  
  const MainPageCell({
    super.key,
    required this.product,
    required this.bgImage  
  });

  @override
  Widget build(BuildContext context) {
    return OpenContainer(
      transitionType: ContainerTransitionType.fade,
      transitionDuration: const Duration(milliseconds: 500),
      closedColor: kBackgroundColor,
      closedElevation: 0,
      clipBehavior: Clip.none,
      closedBuilder: ((context, openDetails) {
        return Container(
        margin: const EdgeInsets.fromLTRB(10, 0, 10, 0),
        height: 100,
        width: 100,
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
        clipBehavior: Clip.hardEdge,
        child: Image(
          image: bgImage,
          fit: BoxFit.contain,
        )
        );
      }),
      openBuilder: ((context, closeDetails) {
        return ProductDetails(productId: int.tryParse(product["id"])!);
      }),
      onClosed: (_){},
    );
  }
}