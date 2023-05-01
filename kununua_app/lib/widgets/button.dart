import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:kununua_app/utils/constants.dart';

class Button extends StatelessWidget {
  final String text;
  final void Function()? action;
  final Color color;
  final EdgeInsets paddingContainer;
  final EdgeInsets paddingButton;
  final Icon? icon;

  const Button({
    super.key,
    required this.text,
    required this.action,
    required this.color,
    this.paddingContainer =
        const EdgeInsets.symmetric(horizontal: 135, vertical: 16),
    this.paddingButton = const EdgeInsets.symmetric(vertical: 14),
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: paddingContainer,
      child: ElevatedButton(
          
          onPressed: action,
          style: ElevatedButton.styleFrom(
            padding: paddingButton,
            shape: const StadiumBorder(),
            backgroundColor: color,
            elevation: 8,
            shadowColor: Colors.black87,
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: icon != null
                ? [
                    icon ?? const Icon(Icons.check),
                    Text(
                      text,
                      style: const TextStyle(
                          fontSize: 18, fontWeight: FontWeight.bold),
                    )
                  ]
                : [
                    Text(
                      text,
                      style: const TextStyle(
                          fontSize: 18, fontWeight: FontWeight.bold),
                    )
                  ],
          )),
    );
  }
}
