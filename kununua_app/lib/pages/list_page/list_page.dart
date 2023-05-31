import 'package:flutter/material.dart';
import 'package:kununua_app/pages/list_page/components/list_extended_view.dart';
import 'package:kununua_app/pages/list_page/components/list_preview.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/requests.dart';

class ListPage extends StatelessWidget {
  const ListPage({super.key});

  Future<List<Map<String, dynamic>>> _getListsView() async {
    List<Map<String, dynamic>> lists = [];

    final QueryOptions getListsQuery = QueryOptions(
      document: gql(getLists),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
      },
    );

    final listResult = await globals.client.value.query(getListsQuery);

    if (listResult.hasException) {
      return [];
    }

    lists = HelperFunctions.deserializeListData(listResult);

    return lists;
  }

  List<Widget> _buildLists(List<Map<String, dynamic>> lists) {
    List<Widget> listPreviews = [];

    for (Map<String, dynamic> list in lists) {
      listPreviews.add(ListPreview(
          date: list['date'].toString(), products: list['productentrySet']));
    }

    return listPreviews;
  }

  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: _getListsView(),
        builder: (context, lists) {
          if (lists.hasData) {
            if ((lists.data ?? []).isEmpty) {
              return const Center(
                child: Text('No tienes ninguna lista creada'),
              );
            } else {
              return ListView(
                children: _buildLists(lists.data!),
              );
            }
          } else {
            return const Center(
              child: CircularProgressIndicator(),
            );
          }
        });
  }
}
