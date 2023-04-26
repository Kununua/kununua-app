import 'package:flutter/material.dart';

class ProductGridFiltersRange extends StatefulWidget {
  final double start;
  final double end;
  final double min;
  final double max;
  final int? divisions;
  final String keyName;
  final Function updateRangedSettedFilters;

  const ProductGridFiltersRange(
      {super.key,
      required this.start,
      required this.end,
      required this.min,
      required this.max,
      this.divisions,
      required this.keyName,
      required this.updateRangedSettedFilters});

  @override
  State<ProductGridFiltersRange> createState() =>
      _ProductGridFiltersRangeState();
}

class _ProductGridFiltersRangeState extends State<ProductGridFiltersRange> {
  RangeValues _values = const RangeValues(0, 100);

  @override
  void initState() {
    _values = RangeValues(widget.start, widget.end);
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return SliderTheme(
        data: const SliderThemeData(
            showValueIndicator: ShowValueIndicator.always),
        child: RangeSlider(
          values: _values,
          min: widget.min,
          max: widget.max,
          divisions: widget.divisions,
          labels: RangeLabels(
            widget.divisions == null
                ? _values.start.toStringAsFixed(2)
                : _values.start.round().toString(),
            widget.divisions == null
                ? _values.end.toStringAsFixed(2)
                : _values.end.round().toString(),
          ),
          onChanged: (RangeValues newValues) {
            setState(() {
              widget.updateRangedSettedFilters(widget.keyName, newValues.start,
                  newValues.end, widget.min, widget.max);
              _values = newValues;
            });
          },
        ));
  }
}
