import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';

class Input extends StatelessWidget {

  final String hint;
  final IconData iconData;

  const Input({
    super.key,
    required this.hint,
    required this.iconData,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 8),
        child: SizedBox(
          height: 50,
          child: Material(
            elevation: 8,
            shadowColor: Colors.black87,
            color: Colors.transparent,
            borderRadius: BorderRadius.circular(30),
            child: TextField(
              textAlignVertical: TextAlignVertical.bottom,
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: BorderSide.none
                ),
                filled: true,
                fillColor: Colors.white,
                hintText: hint,
                prefixIcon: Icon(iconData)
              ),
            ),
          ),
        ),
      );
  }
}