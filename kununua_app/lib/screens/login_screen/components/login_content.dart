import 'package:flutter/material.dart';
import 'package:flutter/src/widgets/container.dart';
import 'package:flutter/src/widgets/framework.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/screens/login_screen/animations/change_screen_animation.dart';
import 'package:kununua_app/screens/login_screen/components/bottom_text.dart';
import 'package:kununua_app/screens/login_screen/components/top_text.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';

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

  Widget inputField(String hint, IconData iconData){
    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 8),
        child: SizedBox(
          height: 50,
          child: Material(
            elevation: 8,
            shadowColor: Colors.black87,
            color: Colors.transparent,
            borderRadius: BorderRadius.circular(30),
            child: TextField(
              textAlignVertical: TextAlignVertical.bottom,
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: BorderSide.none
                ),
                filled: true,
                fillColor: Colors.white,
                hintText: hint,
                prefixIcon: Icon(iconData)
              ),
            ),
          ),
        ),
      );
  }

  Widget loginButton(String title){
    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 135, vertical: 16),
        child: ElevatedButton(
          onPressed: (){},
          style: ElevatedButton.styleFrom(
            padding: const EdgeInsets.symmetric(vertical: 14),
            shape: const StadiumBorder(),
            backgroundColor: kSecondaryColor,
            elevation: 8,
            shadowColor: Colors.black87,
          ),
          child: Text(
            title,
            style: const TextStyle(
              fontSize: 18,
              fontWeight: FontWeight.bold
            ),
          ),
        ),
      );
  }

  Widget orDivider(){
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: 130, vertical: 8),
      child: Row(
        children: [
          Flexible(
            child: Container(
              height: 1,
              color: kPrimaryColor,
              ),
          ),
          const Padding(
            padding: EdgeInsets.symmetric(horizontal: 16),
            child: Text(
              'or',
              style: TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.w600,
              ),
            ),
          ),
          Flexible(
            child: Container(
              height: 1,
              color: kPrimaryColor,
              ),
          ),
        ]
      ),
    );
  }

  Widget logos(){
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

  Widget forgotPassword(){
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 110),
      child: TextButton(
        onPressed: (){},
        child: const Text(
          'Forgot Password?',
          style: TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.w600,
            color: kSecondaryColor,
          ),
        ),
      )
    );
  }

  @override
  void initState() {
    createAccountContent = [
      inputField('Name', Ionicons.person_outline),
      inputField('Email', Ionicons.mail_outline),
      inputField('Password', Ionicons.lock_closed_outline),
      loginButton('Sign Up'),
      orDivider(),
      logos()
    ];

    loginContent = [
      inputField('Email', Ionicons.mail_outline),
      inputField('Password', Ionicons.lock_closed_outline),
      loginButton('Log In'),
      forgotPassword()
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