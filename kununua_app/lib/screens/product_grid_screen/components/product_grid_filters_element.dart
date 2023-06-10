import 'package:flutter/material.dart';

class ProductGridFiltersElement extends StatefulWidget {
  final String name;
  final bool isChecked;
  final String keyName;
  final Function updateNamedSettedFilters;
  const ProductGridFiltersElement(
      {super.key,
      required this.name,
      this.isChecked = false,
      required this.keyName,
      required this.updateNamedSettedFilters});

  @override
  State<ProductGridFiltersElement> createState() =>
      _ProductGridFiltersElementState();
}

class _ProductGridFiltersElementState extends State<ProductGridFiltersElement> {
  bool _isChecked = false;

  @override
  void initState() {
    _isChecked = widget.isChecked;
    super.initState();
  }

  @override
  void didUpdateWidget(covariant ProductGridFiltersElement oldWidget) {
    _isChecked = widget.isChecked;
    super.didUpdateWidget(oldWidget);
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.only(left: 15),
        child: Row(children: [
          Checkbox(
            value: _isChecked,
            onChanged: (bool? value) {
              widget.updateNamedSettedFilters(
                  widget.keyName, widget.name, value);
              setState(() {
                _isChecked = value!;
              });
            },
            fillColor: const MaterialStatePropertyAll(Colors.blue),
          ),
          Text(
            widget.name,
          )
        ]));
  }
}
