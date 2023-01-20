import 'package:flutter/material.dart';
import 'package:kununua_app/screens/main_screen/components/main_page_category_row/main_page_category_cell.dart';
import 'package:kununua_app/screens/main_screen/components/row_title.dart';

class MainPageCategoryRow extends StatelessWidget {
  const MainPageCategoryRow({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
            children: [
              const RowTitle(title: 'Categorías'),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Container(
                  margin: const EdgeInsets.fromLTRB(10, 0, 10, 20),
                  child: Row(
                    children: const [
                      MainPageCategoryCell(
                        categoryName: 'Frescos',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCategoryCell(
                        categoryName: 'Carnicería',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCategoryCell(
                        categoryName: 'Frescos',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCategoryCell(
                        categoryName: 'Frescos',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCategoryCell(
                        categoryName: 'Frescos',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCategoryCell(
                        categoryName: 'Frescos',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCategoryCell(
                        categoryName: 'Frescos',
                        categoryImage: AssetImage('assets/images/frescos.png'),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          );
  }
}