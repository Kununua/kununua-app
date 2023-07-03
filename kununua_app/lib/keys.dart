// ignore_for_file: non_constant_identifier_names

import 'package:flutter/material.dart';
import 'dart:io' show Platform;

String _getBaseLink(){

  String mainGraphqlLink = "http://127.0.0.1:8000/";

  try{
    if (Platform.isAndroid) {
      mainGraphqlLink = "http://10.0.2.2:8000/";
    }

  }catch (e){
    debugPrint("Running in web");
  }

  return mainGraphqlLink;

}
String FLUTTER_APP_API_BASE_URL = '${_getBaseLink()}graphql/';
String FLUTTER_APP_MEDIA_BASE_URL = '${_getBaseLink()}media/';