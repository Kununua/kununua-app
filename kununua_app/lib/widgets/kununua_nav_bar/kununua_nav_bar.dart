import 'package:flutter/material.dart';
import 'package:kununua_app/utils/constants.dart';

import 'components/nav_bar_icon.dart';

enum Screens{
  home,
  stats,
  search,
  cart,
  list,
  profile
}

class KununuaNavBar extends StatefulWidget {
  
  final Screens screen;
  final Function currentScreenCallback;
  
  const KununuaNavBar({
    super.key,
    required this.screen,
    required this.currentScreenCallback
  });

  @override
  State<KununuaNavBar> createState() => _KununuaNavBarState();
}

class _KununuaNavBarState extends State<KununuaNavBar> {
  @override
  Widget build(BuildContext context) {

    final screenSize = MediaQuery.of(context).size;

    return Container(
      width: screenSize.width,
      height: 0.1 * screenSize.height,
      color: kPrimaryColor,
      child: Flex(
        direction: Axis.horizontal,
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          NavBarIcon(
            onPressed: () => {
              widget.currentScreenCallback(Screens.home)
            },
            icon: NavBarIcons.home,
            screen: widget.screen,
          ),
          // NavBarIcon(
          //   onPressed: () => {
          //     widget.currentScreenCallback(Screens.stats)
          //   },
          //   icon: NavBarIcons.stats,
          //   screen: widget.screen,
          // ),
          NavBarIcon(
            onPressed: () => {widget.currentScreenCallback(Screens.search)},
            icon: NavBarIcons.search,
            screen: widget.screen,
          ),
          // NavBarIcon(
          //   onPressed: () => {
          //     widget.currentScreenCallback(Screens.cart)
          //   },
          //   icon: NavBarIcons.cart,
          //   screen: widget.screen,
          // ),
          NavBarIcon(
            onPressed: () => {
              widget.currentScreenCallback(Screens.list)},
            icon: NavBarIcons.list,
            screen: widget.screen,
          ),
          NavBarIcon(
            onPressed: () => {
              widget.currentScreenCallback(Screens.profile)
            },
            icon: NavBarIcons.profile,
            screen: widget.screen,
          ),
        ],
      ),
    );
  }
}