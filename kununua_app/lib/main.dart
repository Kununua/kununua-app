import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/login_screen/login_sceen.dart';
import 'package:kununua_app/screens/main_screen/main_screen.dart';
import 'package:kununua_app/utils/constants.dart';

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
          home: const MainScreen(),             
      ));
  }
}