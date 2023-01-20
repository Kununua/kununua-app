import 'package:flutter/material.dart';
import 'package:kununua_app/screens/main_screen/components/carousel.dart';
import 'package:kununua_app/screens/main_screen/components/main_page_category_row/main_page_category_row.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';
import 'package:kununua_app/screens/main_screen/components/main_page_row/main_page_row.dart';

class MainScreen extends StatelessWidget {
  const MainScreen({super.key});

  @override
  Widget build(BuildContext context) {

    final screenSize = MediaQuery.of(context).size;

    return Scaffold(
      appBar: AppBar(
        title: const Text('K U N U N U A'),
        titleTextStyle: const TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.bold,
        ),
        backgroundColor: kPrimaryColor,
      ),
      body: Stack(
        children: [Container(
          height: screenSize.height,
          width: screenSize.width,
          color: kBackgroundColor,
          padding: EdgeInsets.only(bottom: 0.1 * screenSize.height),
          child: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.max,
              mainAxisAlignment: MainAxisAlignment.center,
              children: const [
                MainCarousel(),
                MainPageCategoryRow(),
                MainPageRow(rowName: 'En oferta'),
                MainPageRow(rowName: 'Volver a comprar'),
                MainPageRow(rowName: 'Productos más vendidos'),
              ],
            ),
          ),
        ),
        const KununuaNavBar(screen: Screens.home),
        ]
      ),
    );
  }
}