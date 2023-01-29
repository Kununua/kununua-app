import 'package:flutter/material.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';

enum NavBarIcons{
  home,
  stats,
  search,
  cart,
  profile
}

class NavBarIcon extends StatelessWidget {
  
  final Screens screen;
  final NavBarIcons icon;
  final VoidCallback? onPressed;
  
  const NavBarIcon({
    super.key,
    required this.icon,
    required this.screen,
    this.onPressed,
  });

  bool _isScreen(){
    return screen.toString().split(".")[1] == icon.toString().split(".")[1];
  }

  IoniconsData? _getIcon(){
    
    if (_isScreen()){
      if (icon == NavBarIcons.home) return Ionicons.home;
      if (icon == NavBarIcons.stats) return Ionicons.stats_chart;
      if (icon == NavBarIcons.search) return Ionicons.search;
      if (icon == NavBarIcons.cart) return Ionicons.cart;
      if (icon == NavBarIcons.profile) return Ionicons.person;
      return null;
    }else{
      if (icon == NavBarIcons.home) return Ionicons.home_outline;
      if (icon == NavBarIcons.stats) return Ionicons.stats_chart_outline;
      if (icon == NavBarIcons.search) return Ionicons.search_outline;
      if (icon == NavBarIcons.cart) return Ionicons.cart_outline;
      if (icon == NavBarIcons.profile) return Ionicons.person_outline;
      return null;
    }
  }

  @override
  Widget build(BuildContext context) {

    return Container(
              decoration: BoxDecoration(
                border: Border(
                  top: BorderSide(
                    color: _isScreen() ? Colors.white : Colors.transparent,
                    width: 3,
                  ),
                ),
              ),
              child: IconButton(
                onPressed: onPressed,
                icon: Icon(
                  _getIcon(),
                  color: Colors.white,
                  size: 30,
                ),
              ),
            );
  }
}