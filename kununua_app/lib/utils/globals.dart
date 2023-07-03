library kununua.globals;

import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/keys.dart';
import 'package:shared_preferences/shared_preferences.dart';

ValueNotifier<GraphQLClient> client = ValueNotifier(GraphQLClient(cache: GraphQLCache(), link: HttpLink(FLUTTER_APP_API_BASE_URL)));
SharedPreferences? prefs;