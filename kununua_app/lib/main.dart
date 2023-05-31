import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:intl/intl.dart';
import 'package:kununua_app/pages/welcome_page.dart';
import 'package:kununua_app/screens/new_login_screen/login_screen.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/screens/product_details_screen/product_details_screen.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/requests.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:intl/date_symbol_data_local.dart';

void main() {
  SystemChrome.setSystemUIOverlayStyle(
    SystemUiOverlayStyle(
      systemNavigationBarColor:
          SystemUiOverlayStyle.dark.systemNavigationBarColor,
    ),
  );
  initializeDateFormatting('es', null);
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  Future<bool> checkToken() async {
    bool validToken = false;

    var prefs = await SharedPreferences.getInstance();

    globals.prefs = prefs;

    final MutationOptions refreshTokenOptions = MutationOptions(
      document: gql(refreshToken),
      variables: <String, dynamic>{
        'token': globals.prefs!.getString('jwtToken') ?? '',
      },
    );

    final tokenResult = await globals.client.value.mutate(refreshTokenOptions);

    if (!tokenResult.hasException) {
      validToken = true;
      globals.prefs!
          .setString('jwtToken', tokenResult.data!['refreshToken']['token']);
    }

    return validToken;
  }

  @override
  Widget build(BuildContext context) {
    return GraphQLProvider(
        client: globals.client,
        child: MaterialApp(
          debugShowCheckedModeBanner: false,
          title: 'Kununua',
          theme: ThemeData(
            scaffoldBackgroundColor: kBackgroundColor,
            textTheme: Theme.of(context)
                .textTheme
                .apply(bodyColor: kPrimaryColor, fontFamily: 'Montserrat'),
          ),
          home: FutureBuilder(
            future: checkToken(),
            builder: (context, snapshot) {
              if (snapshot.hasData) {
                if (snapshot.data!) {
                  return const MainScreen();
                } else {
                  return const LoginScreen();
                }
              } else {
                return const Center(
                  child: CircularProgressIndicator(),
                );
              }
            },
          ),
        ));
  }
}
