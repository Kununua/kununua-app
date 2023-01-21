import 'package:flutter/material.dart';
import 'package:kununua_app/utils/constants.dart';

class MainPageAppBar extends StatefulWidget implements PreferredSizeWidget {
  const MainPageAppBar({super.key});

  @override
  State<MainPageAppBar> createState() => _MainPageAppBarState();
  
  @override
  Size get preferredSize => const Size.fromHeight(50);
}

class _MainPageAppBarState extends State<MainPageAppBar> {
  @override
  Widget build(BuildContext context) {
    return AppBar(
        title: const Text('K U N U N U A'),
        titleTextStyle: const TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
        backgroundColor: kPrimaryColor,
      );
  }
}