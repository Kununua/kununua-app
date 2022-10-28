import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/screens/login_screen/animations/change_screen_animation.dart';
import 'package:kununua_app/screens/login_screen/components/bottom_text.dart';
import 'package:kununua_app/screens/login_screen/components/top_text.dart';
import 'package:kununua_app/screens/login_screen/widgets/forgot_password.dart';
import 'package:kununua_app/screens/login_screen/widgets/logos.dart';
import 'package:kununua_app/screens/login_screen/widgets/or_divider.dart';
import 'package:kununua_app/screens/welcome_screen/welcome_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/widgets/button.dart';
import 'package:kununua_app/utils/widgets/input.dart';
enum Screens{
  createAccount,
  welcomeBack
}

class LoginContent extends StatefulWidget {
  
  const LoginContent({super.key});

  @override
  State<LoginContent> createState() => _LoginContentState();
}

class _LoginContentState extends State<LoginContent> with TickerProviderStateMixin {

  late final List<Widget> createAccountContent;
  late final List<Widget> loginContent;

  void _register() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const WelcomeScreen(),
      ),
    );
  }

  void _login() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const WelcomeScreen(),
      ),
    );
  }

  @override
  void initState() {
    createAccountContent = [
      const Input(
        hint: 'Name', 
        iconData: Ionicons.person_outline
      ),
      const Input(
        hint: 'Email', 
        iconData: Ionicons.mail_outline
      ),
      const Input(
        hint: 'Password', 
        iconData: Ionicons.lock_closed_outline
      ),
      Button(
        text: 'Sign Up', 
        action: _register,
        color: kSecondaryColor,  
      ),
      const OrDivider(),
      const Logos(),
    ];

    loginContent = [
      const Input(
        hint: 'Email', 
        iconData: Ionicons.mail_outline
      ),
      const Input(
        hint: 'Password', 
        iconData: Ionicons.lock_closed_outline
      ),
      Button(
        text: 'Log In', 
        action: _login,
        color: kSecondaryColor,  
      ),
      const ForgotPassword(),
    ];

    ChangeScreenAnimation.initialize(
      vsync: this,
      createAccountItems: createAccountContent.length,
      loginItems: loginContent.length
    );

    for(var i = 0; i<createAccountContent.length; i++){
      createAccountContent[i] = HelperFunctions.wrapWithAnimatedBuilder(
        animation: ChangeScreenAnimation.createAccountAnimation[i], 
        child: createAccountContent[i]
      );
    }

    for(var i = 0; i<loginContent.length; i++){
      loginContent[i] = HelperFunctions.wrapWithAnimatedBuilder(
        animation: ChangeScreenAnimation.loginAnimation[i], 
        child: loginContent[i]
      );
    }

    super.initState();
  }

  @override
  void dispose() {
    ChangeScreenAnimation.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {

    return Stack(
      children: [
        const Positioned(
          top: 136,
          left: 24,
          child: TopText()
        ),
        Padding(
          padding: const EdgeInsets.only(top: 100),
          child: Stack(
            children: [
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: createAccountContent,
              ),
              Column(
                mainAxisAlignment: MainAxisAlignment.center,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: loginContent,
              ),
            ]
          ),
        ),
        const Align(
          alignment: Alignment.bottomCenter,
          child: Padding(
            padding: EdgeInsets.only(bottom: 50),
            child: BottomText(),
          ),
        ),
      ],
    );
  }
}