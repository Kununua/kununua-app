import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:kununua_app/screens/login_screen/animations/change_screen_animation.dart';
import 'package:kununua_app/screens/login_screen/components/login_content.dart';
import 'package:kununua_app/screens/login_screen/login_sceen.dart';
import 'package:kununua_app/utils/widgets/button.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen> {

  void _return(){;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const LoginScreen(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Center(child: Text('Welcome Screen')),
            Button(text: 'Volver', action: _return, color: Color.fromARGB(255, 255, 0, 0))
          ],
        ),
      ),
    );
  }
}