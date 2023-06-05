import 'package:flutter/material.dart';

class KununuaGrid extends StatelessWidget {
  final List<Widget> children;
  final int crossAxisCount;
  final MainAxisAlignment mainAxisAlignment;
  final CrossAxisAlignment crossAxisAlignment;
  final double mainAxisSpacing;
  final double crossAxisSpacing;
  final EdgeInsets gridMargin;
  final bool scrollable;
  final ScrollController? scrollController;

  const KununuaGrid({
    super.key,
    required this.children,
    this.crossAxisCount = 4,
    this.crossAxisAlignment = CrossAxisAlignment.start,
    this.mainAxisAlignment = MainAxisAlignment.spaceEvenly,
    this.mainAxisSpacing = 5,
    this.crossAxisSpacing = 0,
    this.gridMargin = const EdgeInsets.all(0),
    this.scrollable = false,
    this.scrollController,
  });

  @override
  Widget build(BuildContext context) {
    List<Container> rows = [];

    for (var i = 0; i < children.length; i += crossAxisCount) {
      try {
        rows.add(Container(
          margin: EdgeInsets.fromLTRB(crossAxisSpacing, mainAxisSpacing,
              crossAxisSpacing, mainAxisSpacing),
          child: Row(
            mainAxisAlignment: mainAxisAlignment,
            children: children.sublist(i, i + crossAxisCount),
          ),
        ));
      } catch (e) {
        rows.add(Container(
          margin: EdgeInsets.fromLTRB(crossAxisSpacing, mainAxisSpacing,
              crossAxisSpacing, mainAxisSpacing),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: children.sublist(i, children.length),
          ),
        ));
      }
    }

    if (!scrollable) {
      return Container(
        margin: gridMargin,
        child: Column(
          crossAxisAlignment: crossAxisAlignment,
          children: rows,
        ),
      );
    }

    return Container(
      margin: gridMargin,
      child: SingleChildScrollView(
        controller: scrollController,
        scrollDirection: Axis.vertical,
        child: Column(
          crossAxisAlignment: crossAxisAlignment,
          children: rows,
        ),
      ),
    );
  }
}
