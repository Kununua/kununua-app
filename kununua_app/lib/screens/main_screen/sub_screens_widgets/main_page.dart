import 'package:flutter/material.dart';
import 'package:kununua_app/screens/main_screen/components/main_page_category_row/main_page_category_row.dart';
import 'package:kununua_app/screens/main_screen/components/carousel.dart';
import 'package:kununua_app/screens/main_screen/components/main_page_row/main_page_row.dart';
import 'package:kununua_app/utils/constants.dart';


class MainPage extends StatelessWidget {
  const MainPage({super.key});

  @override
  Widget build(BuildContext context) {

    final screenSize = MediaQuery.of(context).size;

    return Container(
        height: screenSize.height,
        width: screenSize.width,
        color: kBackgroundColor,
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
      );
  }
}