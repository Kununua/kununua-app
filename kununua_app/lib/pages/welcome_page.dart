import 'package:flutter/material.dart';
import 'package:kununua_app/screens/login_screen/login_sceen.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:shared_preferences/shared_preferences.dart';

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

  Future<String> _getNameFromLocalStorage() async{
    final localStorage = await SharedPreferences.getInstance();
    return localStorage.getString('username') ?? '';
  }

  @override
  void initState() { 

    _getNameFromLocalStorage().then((value) => {
      setState(() {
        name = value;
      })
    });

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
            Button(text: 'Volver', action: _return, color: Color.fromARGB(255, 255, 0, 0))
          ],
        ),
      ),
    );
  }
}