library kununua.globals;
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

final HttpLink mainGraphqlLink = HttpLink("http://127.0.0.1:8000/graphql/");

ValueNotifier<GraphQLClient> client = ValueNotifier(GraphQLClient(cache: GraphQLCache(), link: mainGraphqlLink));