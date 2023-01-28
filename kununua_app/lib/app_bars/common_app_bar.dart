import 'package:flutter/material.dart';
import 'package:kununua_app/utils/constants.dart';

class CommonAppBar extends StatelessWidget implements PreferredSizeWidget {
  
  final String text;
  
  const CommonAppBar({
    super.key,
    required this.text,
  });

  @override
  Widget build(BuildContext context) {
    return AppBar(
        title: Text(text.toUpperCase()),
        titleTextStyle: const TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
        backgroundColor: kPrimaryColor,
      );
  }

  @override
  Size get preferredSize => const Size.fromHeight(50);
}