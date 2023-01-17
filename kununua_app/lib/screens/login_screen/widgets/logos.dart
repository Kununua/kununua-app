import 'package:flutter/material.dart';

class Logos extends StatefulWidget {
  const Logos({super.key});

  @override
  State<Logos> createState() => _LogosState();
}

class _LogosState extends State<Logos> {
  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 16),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Image.asset('assets/images/facebook.png'),
          const SizedBox(width: 24),
          Image.asset('assets/images/google.png'),
        ],
      ),
    );
  }
}