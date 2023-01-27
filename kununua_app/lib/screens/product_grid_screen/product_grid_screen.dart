import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/common_app_bar.dart';
import 'package:kununua_app/utils/constants.dart';

class ProductGridScreen extends StatelessWidget {

  final String category;

  const ProductGridScreen({
    super.key,
    required this.category,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CommonAppBar(
        text: category,
      ),
      body: Center(
        child: Container(
          color: kBackgroundColor,
          child: Text('Not implemented yet. The category is: $category'),
        ),
      ),
    );
  }
}