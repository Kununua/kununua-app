library kununua.globals;
import 'dart:io' show Platform;

import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

HttpLink _getLink(){

  HttpLink mainGraphqlLink = HttpLink("http://127.0.0.1:8000/graphql/");

  try{
    if (Platform.isAndroid) {
      mainGraphqlLink = HttpLink("http://10.0.2.2:8000/graphql/");
    }

  }catch (e){
    debugPrint("Running in web");
  }

  return mainGraphqlLink;

}

ValueNotifier<GraphQLClient> client = ValueNotifier(GraphQLClient(cache: GraphQLCache(), link: _getLink()));
String jwtToken = '';
Map<String, dynamic> currentUser = <String, dynamic>{};