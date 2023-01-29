import 'package:flutter/material.dart';
import 'package:kununua_app/pages/main_page/components/main_page_category_row/main_page_category_cell.dart';
import 'package:kununua_app/pages/main_page/components/row_title.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

class MainPageCategoryRow extends StatelessWidget {
  const MainPageCategoryRow({super.key});

  Future<List<Map<String, dynamic>>> _getCategories() async{

    List<Map<String, dynamic>> categories = [];

    final MutationOptions getAllCategoriesOptions = MutationOptions(
      document: gql(getCategories),
    );

    final categoriesResult = await globals.client.value.mutate(getAllCategoriesOptions);

    var categoriesList = categoriesResult.data!['getAllCategories'];

    for (var category in categoriesList){
      categories.add({
        'name': category['name'],
      });
    }

    return categories;
  }

  @override
  Widget build(BuildContext context) {

    List<Widget> loadingChildren = [];

    for (var i = 0; i < 7; i++){
      loadingChildren.add(
        const MainPageCategoryCell(
          isLoading: true,
        ),
      );
    }

    return Column(
            children: [
              const RowTitle(title: 'Categorías'),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Container(
                  margin: const EdgeInsets.fromLTRB(10, 0, 10, 20),
                  child: FutureBuilder(
                    future: _getCategories(),
                    builder: (BuildContext context, AsyncSnapshot snapshot){
                      if (snapshot.hasData){
                        return Row(
                          children: snapshot.data.map<Widget>((category) => MainPageCategoryCell(
                            categoryName: category['name'],
                            categoryImage: const AssetImage('assets/images/frescos.png'),
                          )).toList(),
                        );
                      } else {
                        return Row(
                          children: loadingChildren,
                        );
                      }
                    },
                  ),
                ),
              ),
            ],
          );
  }
}