import 'package:flutter/material.dart';

class ProductGridFiltersTitle extends StatelessWidget {
  final String name;

  const ProductGridFiltersTitle({super.key, required this.name});

  @override
  Widget build(BuildContext context) {
    return Text(name.toUpperCase());
  }
}
