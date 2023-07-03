import 'package:flutter/material.dart';
import 'package:kununua_app/screens/new_login_screen/login_screen.dart';
import '../widgets/button.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class WelcomePage extends StatefulWidget {
  const WelcomePage({super.key});

  @override
  State<WelcomePage> createState() => _WelcomePageState();
}

class _WelcomePageState extends State<WelcomePage> {

  String name = '';

  void _return(){;
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const LoginScreen(),
      ),
    );
  }

  @override
  void initState() {

    name = globals.prefs!.getString('username') as String;

    super.initState();
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Center(child: Text('Welcome $name')),
            Button(text: 'Volver', action: _return, color: const Color.fromARGB(255, 255, 0, 0))
          ],
        ),
      ),
    );
  }
}