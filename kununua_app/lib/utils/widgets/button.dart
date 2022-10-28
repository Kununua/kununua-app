import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:kununua_app/utils/constants.dart';

class Button extends StatelessWidget {
  
  final String text;
  final void Function() action;
  final Color color;
  
  const Button({
    super.key,
    required this.text,
    required this.action,
    required this.color,  
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 135, vertical: 16),
        child: ElevatedButton(
          onPressed: action,
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: const StadiumBorder(),
            backgroundColor: kSecondaryColor,
            elevation: 8,
            shadowColor: Colors.black87,
          ),
          child: Text(
            text,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold
            ),
          ),
        ),
      );;
  }
}