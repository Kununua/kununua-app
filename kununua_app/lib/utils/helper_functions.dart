import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';


class HelperFunctions{

  static Map<String, dynamic> deserializeData(QueryResult<Object?> queryResult){

  Map<String, dynamic> result = {};

  String operationName = queryResult.data!.keys.elementAt(1);
  Map<String, dynamic> data = queryResult.data![operationName];
  
  for (String key in data.keys) {
    
    if(key != 'image' && key != '__typename' && key != 'supermarket'){
      var value = data[key];
      if(value.runtimeType == Map<String, dynamic>){
        result[key] = _recursiveDeserialization(value);
      }else{
        result[key] = value;
      }
    } 
  }
  
  data['image'] = HelperFunctions._getImage(data['image']);

  return data;
}

static Map<String, dynamic> _recursiveDeserialization(Map<String, dynamic> data){
  Map<String, dynamic> serializedData = {};
  for (String key in data.keys) {
    if(key != '__typename' && key != 'image'){
      var value = data[key];
      if(value.runtimeType == Map<String, dynamic>){
        serializedData[key] = _recursiveDeserialization(value);
      }else{
        serializedData[key] = value;
      }
    }
  }

  serializedData['image'] = HelperFunctions._getImage(data['image']);

  return serializedData;
}

static ImageProvider _getImage(encodedImage){
  return MemoryImage(base64Decode(encodedImage));
}
}
