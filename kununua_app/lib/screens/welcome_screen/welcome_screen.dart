import 'package:flutter/material.dart';
import 'package:kununua_app/screens/new_login_screen/login_screen.dart';
import 'package:kununua_app/utils/widgets/button.dart';
import 'package:shared_preferences/shared_preferences.dart';

class WelcomeScreen extends StatefulWidget {
  const WelcomeScreen({super.key});

  @override
  State<WelcomeScreen> createState() => _WelcomeScreenState();
}

class _WelcomeScreenState extends State<WelcomeScreen> {

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