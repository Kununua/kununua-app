import 'dart:ui';

import 'package:flutter/material.dart';

class CenterWidgetPainter extends CustomPainter {

  final Path path;

  CenterWidgetPainter({required this.path});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = Colors.black26
      ..style = PaintingStyle.stroke
      ..strokeWidth = 10
      ..imageFilter = ImageFilter.blur(sigmaX: 10, sigmaY: 10);

    canvas.drawPath(path, paint);
  }

  @override
  bool shouldRepaint(CenterWidgetPainter oldDelegate) => false;
}