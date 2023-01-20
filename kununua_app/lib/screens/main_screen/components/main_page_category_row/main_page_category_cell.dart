import 'package:flutter/material.dart';
import 'package:blurrycontainer/blurrycontainer.dart';

class MainPageCategoryCell extends StatelessWidget {
  
  final String categoryName;
  final ImageProvider categoryImage;

  const MainPageCategoryCell({
    super.key,
    required this.categoryName,
    required this.categoryImage,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.fromLTRB(10, 0, 10, 0),
      height: 150,
      width: 150,
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
      child: Stack(
        children: [
          Image(
            image: categoryImage,
            fit: BoxFit.cover,
          ),
          Center(
            child: BlurryContainer(
              padding: const EdgeInsets.fromLTRB(10, 5, 10, 5),
              color: Color.fromARGB(118, 255, 255, 255),
              blur: 5,
              borderRadius: const BorderRadius.all(Radius.circular(10)),
              child: Text(
                categoryName,
                style: const TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                  ),
                )
            )
          )
        ],
      )
      );
  }
}