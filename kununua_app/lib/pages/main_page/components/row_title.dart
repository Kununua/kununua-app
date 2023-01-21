import 'package:flutter/material.dart';

class RowTitle extends StatelessWidget {
  
  final String title;
  
  const RowTitle({
    super.key,
    required this.title  
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
                padding: const EdgeInsets.fromLTRB(20, 0, 0, 20),
                child: Row(
                  children: [
                    Text(
                      title,
                      style: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              );
  }
}