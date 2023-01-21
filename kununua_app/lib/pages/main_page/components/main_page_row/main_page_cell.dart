import 'package:flutter/material.dart';

class MainPageCell extends StatelessWidget {
  
  final ImageProvider bgImage;
  
  const MainPageCell({
    super.key,
    required this.bgImage  
  });

  @override
  Widget build(BuildContext context) {
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
      child: Image(
        image: bgImage,
        fit: BoxFit.contain,
      )
      );
  }
}