import 'package:flutter/animation.dart';
import 'package:kununua_app/screens/login_screen/components/login_content.dart';

class ChangeScreenAnimation{
  static late AnimationController topTextController;
  static late Animation<Offset> topTextAnimation;

  static late AnimationController bottomTextController;
  static late Animation<Offset> bottomTextAnimation;

  static List<AnimationController> createAccountControllers = [];
  static List<Animation<Offset>> createAccountAnimation = [];

  static List<AnimationController> loginControllers = [];
  static List<Animation<Offset>> loginAnimation = [];

  static var isPlaying = false;
  static var currentScreen = Screens.welcomeBack;

  static Animation<Offset> _createAnimation({
    required Offset begin,
    required Offset end,
    required AnimationController parent,
  }){
    return Tween(begin: begin, end: end,).animate(
      CurvedAnimation(
        parent: parent,
        curve: Curves.easeInOut,
      ),
    );
  }

  static void initialize({
    required TickerProvider vsync,
    required int createAccountItems,
    required int loginItems
  }){

    createAccountControllers = [];
    createAccountAnimation = [];

    loginControllers = [];
    loginAnimation = [];

    isPlaying = false;
    currentScreen = Screens.welcomeBack;

    topTextController = AnimationController(
      vsync: vsync,
      duration: const Duration(milliseconds: 200),
    );

    topTextAnimation = _createAnimation(
      begin: Offset.zero,
      end: const Offset(-1.2, 0),
      parent: topTextController,
    );

    bottomTextController = AnimationController(
      vsync: vsync,
      duration: const Duration(milliseconds: 200),
    );

    bottomTextAnimation = _createAnimation(
      begin: Offset.zero,
      end: const Offset(0, -1.7),
      parent: bottomTextController,
    );

    for(var i = 0; i<loginItems; i++){
      loginControllers.add(AnimationController(
        vsync: vsync,
        duration: const Duration(milliseconds: 200),
      ));

      loginAnimation.add(_createAnimation(
        begin: Offset.zero,
        end: const Offset(-1, 0),
        parent: loginControllers[i],
      ));
    }

    for(var i = 0; i<createAccountItems; i++){
      createAccountControllers.add(AnimationController(
        vsync: vsync,
        duration: const Duration(milliseconds: 200),
      ));

      createAccountAnimation.add(_createAnimation(
        begin: const Offset(1, 0),
        end: Offset.zero,
        parent: createAccountControllers[i],
      ));
    }
  }

  static void dispose(){
    for(final controller in [topTextController, bottomTextController, 
    ...createAccountControllers, ...loginControllers]){
      controller.dispose();
    }
  }

  static Future<void> forward() async{

    isPlaying = true;

    topTextController.forward();
    await bottomTextController.forward();

    for(final controller in [...loginControllers, ...createAccountControllers]){
      controller.forward();
      await Future.delayed(const Duration(milliseconds: 100));
    }

    bottomTextController.reverse();
    await topTextController.reverse();

    isPlaying = false;
  } 

  static Future<void> reverse() async{

    isPlaying = true;

    topTextController.forward();
    await bottomTextController.forward();

    for(final controller in [...createAccountControllers.reversed, ...loginControllers.reversed]){
      controller.reverse();
      await Future.delayed(const Duration(milliseconds: 100));
    }

    bottomTextController.reverse();
    await topTextController.reverse();

    isPlaying = false;
  } 
}