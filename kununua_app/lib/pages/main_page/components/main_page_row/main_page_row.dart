import 'package:flutter/material.dart';
import 'package:kununua_app/pages/main_page/components/main_page_row/main_page_cell.dart';
import 'package:kununua_app/pages/main_page/components/row_title.dart';

class MainPageRow extends StatelessWidget {
  
  final List<Widget> cells;
  final String rowName;
  final bool loading;
  
  const MainPageRow({
    super.key,
    required this.rowName,
    this.cells = const [],
    this.loading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Visibility(
      visible: cells.isNotEmpty,
      child: Column(
              children: [
                RowTitle(title: rowName),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Container(
                    margin: const EdgeInsets.fromLTRB(10, 0, 10, 20),
                    child: loading ? 
                    const Center(
                      child: CircularProgressIndicator(),
                    )
                    :
                    Row(
                      children: cells,
                    ),
                  ),
                ),
              ],
            ),
    );
  }
}