import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/new_login_screen/login_screen.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/screens/product_details_screen.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

void main() {
  SystemChrome.setSystemUIOverlayStyle(
    SystemUiOverlayStyle(
      systemNavigationBarColor:
          SystemUiOverlayStyle.dark.systemNavigationBarColor,
    ),
  );
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {

    return GraphQLProvider(
        client: globals.client,
        child: MaterialApp(  
          debugShowCheckedModeBanner: false,        
          title: 'Kununua App',
          theme: ThemeData(           
            scaffoldBackgroundColor: kBackgroundColor,
            textTheme: Theme.of(context).textTheme.apply(
              bodyColor: kPrimaryColor,
              fontFamily: 'Montserrat'
            ),
          ), 
          // home: MainScreen(),
          home: const ProductDetails(
            productImage: AssetImage('assets/images/products/pechuga.png'),
            productName: "Pechuga de pavo"
          ),             
      ));
  }
}