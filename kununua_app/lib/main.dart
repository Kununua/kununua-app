import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'screens/login_screen/login_sceen.dart';
import 'screens/main_screen.dart';
import 'utils/constants.dart';

import 'screens/product_details_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {

    final HttpLink link = HttpLink("http://127.0.0.1:8000/graphql/");

    ValueNotifier<GraphQLClient> client = ValueNotifier(GraphQLClient(cache: GraphQLCache(), link: link));

    return GraphQLProvider(
        client: client,
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
          home: MainScreen(),
          // home: const ProductDetails(
          //   productImage: AssetImage('assets/images/products/pechuga.png'),
          //   productName: "Pechuga de pavo"
          // ),             
      ));
  }
}