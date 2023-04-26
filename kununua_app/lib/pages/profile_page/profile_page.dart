import 'package:flutter/material.dart';
import 'package:kununua_app/screens/new_login_screen/login_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Flex(
      direction: Axis.vertical,
      mainAxisAlignment: MainAxisAlignment.center,
      crossAxisAlignment: CrossAxisAlignment.center,
      children: [
        Button(
          text: "Cerrar sesión",
          color: Colors.red,
          paddingContainer: const EdgeInsets.fromLTRB(100, 0, 100, 0),
          action: () {
            globals.prefs!.remove('jwtToken');
            globals.prefs!.remove('username');
            globals.prefs!.remove('email');
            globals.prefs!.remove('firstName');
            globals.prefs!.remove('lastName');

            Navigator.of(context).pushReplacement(
              MaterialPageRoute(
                builder: (context) => const LoginScreen(),
              ),
            );
          },
        )
      ],
    );
  }
}
