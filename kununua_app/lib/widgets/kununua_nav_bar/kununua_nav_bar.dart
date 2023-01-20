import 'package:flutter/material.dart';
import 'package:kununua_app/utils/constants.dart';

import 'components/nav_bar_icon.dart';

enum Screens{
  home,
  stats,
  search,
  cart,
  profile
}

class KununuaNavBar extends StatelessWidget {
  
  final Screens screen;
  
  const KununuaNavBar({
    super.key,
    required this.screen
  });

  @override
  Widget build(BuildContext context) {

    final screenSize = MediaQuery.of(context).size;

    return Positioned(
      bottom: 0,
      left: 0,
      child: Container(
        width: screenSize.width,
        height: 0.1 * screenSize.height,
        color: kPrimaryColor,
        child: Flex(
          direction: Axis.horizontal,
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            NavBarIcon(
              onPressed: () => {debugPrint("Pressed home")},
              icon: NavBarIcons.home,
              screen: screen,
            ),
            NavBarIcon(
              onPressed: () => {debugPrint("Pressed stats")},
              icon: NavBarIcons.stats,
              screen: screen,
            ),
            NavBarIcon(
              onPressed: () => {debugPrint("Pressed search")},
              icon: NavBarIcons.search,
              screen: screen,
            ),
            NavBarIcon(
              onPressed: () => {debugPrint("Pressed cart")},
              icon: NavBarIcons.cart,
              screen: screen,
            ),
            NavBarIcon(
              onPressed: () => {debugPrint("Pressed profile")},
              icon: NavBarIcons.profile,
              screen: screen,
            ),
          ],
        ),
      ),
    );
  }
}