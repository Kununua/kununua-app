import 'package:flutter/material.dart';
import 'package:kununua_app/screens/login_screen/animations/change_screen_animation.dart';
import 'package:kununua_app/screens/login_screen/components/login_content.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';

class BottomText extends StatefulWidget {

  const BottomText({
    super.key,
  });

  @override
  State<BottomText> createState() => _BottomTextState();
}

class _BottomTextState extends State<BottomText> {

  @override
  void initState() {
    ChangeScreenAnimation.bottomTextAnimation.addStatusListener((status) {
      if(status == AnimationStatus.completed){
        setState(() {});
      }
    });
    super.initState();
  }


  @override
  Widget build(BuildContext context) {
    return HelperFunctions.wrapWithAnimatedBuilder(
      animation: ChangeScreenAnimation.bottomTextAnimation,
      child: GestureDetector(
        onTap: (){
          if(!ChangeScreenAnimation.isPlaying){
            ChangeScreenAnimation.currentScreen == Screens.welcomeBack ?
            ChangeScreenAnimation.forward()
            :
            ChangeScreenAnimation.reverse();

            ChangeScreenAnimation.currentScreen = 
                          Screens.values[1 - ChangeScreenAnimation.currentScreen.index];
          }
        },
        behavior: HitTestBehavior.opaque,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: RichText(
            text: TextSpan(
              style: const TextStyle(
                fontSize: 16,
                fontFamily: 'Montserrat',
              ),
              children: [
                TextSpan(
                  text: ChangeScreenAnimation.currentScreen == Screens.welcomeBack
                      ? 'Don\'t have an account? '
                      : 'Already have an account? ',
                  style: const TextStyle(
                    color: kPrimaryColor,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                TextSpan(
                  text: ChangeScreenAnimation.currentScreen == Screens.welcomeBack ? 'Sign Up' : 'Log In',
                  style: const TextStyle(
                    color: kSecondaryColor,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}