import 'package:flutter/material.dart';
import 'package:kununua_app/pages/main_page/components/main_page_row/main_page_cell.dart';
import 'package:kununua_app/pages/main_page/components/row_title.dart';

class MainPageRow extends StatelessWidget {
  
  final String rowName;
  
  const MainPageRow({
    super.key,
    required this.rowName
  });

  @override
  Widget build(BuildContext context) {
    return Column(
            children: [
              RowTitle(title: rowName),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Container(
                  margin: const EdgeInsets.fromLTRB(10, 0, 10, 20),
                  child: Row(
                    children: const [
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                      MainPageCell(
                        bgImage: AssetImage('assets/images/frescos.png'),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          );
  }
}