// Copyright 2018 The Flutter team. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

import 'package:flutter/material.dart';
import 'package:kununua_app/screens/login_screen/login_sceen.dart';
import 'package:kununua_app/utils/constants.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(  
      debugShowCheckedModeBanner: false,        
      title: 'Kununua App',
      theme: ThemeData(           
        scaffoldBackgroundColor: kBackgroundColor,
        textTheme: Theme.of(context).textTheme.apply(
          bodyColor: kPrimaryColor,
          fontFamily: 'Montserrat'
        ),
      ), 
      home: const LoginScreen(),             
    );
  }
}