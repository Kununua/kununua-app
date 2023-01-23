import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

const  List<String> imageKeys = ['image', 'profilePicture'];

class HelperFunctions{

  static Map<String, dynamic> deserializeData(QueryResult<Object?> queryResult){

    String operationName = queryResult.data!.keys.elementAt(1);
    Map<String, dynamic> data = queryResult.data![operationName];
    
    Map<String, dynamic> result = _recursiveDeserialization(data);

    return result;
  }

  static Map<String, dynamic> _recursiveDeserialization(Map<String, dynamic> data){
    Map<String, dynamic> serializedData = {};
    for (String key in data.keys) {
      if(imageKeys.contains(key)){
        serializedData[key] = HelperFunctions._getImage(data[key]);
      }else if(key != '__typename'){
        var value = data[key];
        if(value.runtimeType == Map<String, dynamic>){
          serializedData[key] = _recursiveDeserialization(value);
        }else{
          serializedData[key] = value;
        }
      }
    }

    return serializedData;
  }

  static ImageProvider _getImage(encodedImage){
    return MemoryImage(base64Decode(encodedImage));
  }
}
