import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/keys.dart';

const List<String> imageKeys = ['image', 'profilePicture'];

class HelperFunctions {
  static List<Map<String, dynamic>> deserializeListData(
      QueryResult<Object?> queryResult,
      {String? otherOperationName}) {
    String operationName = queryResult.data!.keys.elementAt(1);

    final data = otherOperationName != null
        ? queryResult.data![operationName]![otherOperationName]
        : queryResult.data![operationName];

    List<Map<String, dynamic>> result = [];

    for (final dataEntry in data) {
      result.add(_recursiveDeserialization(dataEntry as Map<String, dynamic>));
    }

    return result;
  }

  static Map<String, dynamic> deserializeData(
      QueryResult<Object?> queryResult) {
    String operationName = queryResult.data!.keys.elementAt(1);
    Map<String, dynamic> data = queryResult.data![operationName];

    Map<String, dynamic> result = _recursiveDeserialization(data);

    return result;
  }

  static Map<String, dynamic> _recursiveDeserialization(
      Map<String, dynamic> data) {
    Map<String, dynamic> serializedData = {};
    for (String key in data.keys) {
      if (imageKeys.contains(key)) {
        serializedData[key] = HelperFunctions._getImage(data[key]);
      } else if (key != '__typename') {
        var value = data[key];
        if (value is Map<String, dynamic>) {
          serializedData[key] = _recursiveDeserialization(value);
        } else {
          serializedData[key] = value;
        }
      }
    }

    return serializedData;
  }

  static ImageProvider _getImage(image) {
    return NetworkImage(FLUTTER_APP_MEDIA_BASE_URL + image);
  }
}
