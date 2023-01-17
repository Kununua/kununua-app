import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
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
import 'package:shared_preferences/shared_preferences.dart';

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

  final _registerFormKey = GlobalKey<FormState>();
  final _loginFormKey = GlobalKey<FormState>();

  final TextEditingController _registerEmailController = TextEditingController();
  final TextEditingController _registerUsernameController = TextEditingController();
  final TextEditingController _registerPasswordController = TextEditingController();

  final TextEditingController _loginUsernameController = TextEditingController();
  final TextEditingController _loginPasswordController = TextEditingController();

  bool _keyboard_toggling = true;

  @override
  void initState() {

    String createUser = """
       mutation createUser(\$username: String!, \$password: String!, \$email: String!){
        createUser(username: \$username, password: \$password, email: \$email){
          user{
            username
          }
        }
      }
    """;

    String logUser = """
       query logUser(\$username: String!, \$password: String!){
          logUser(username: \$username, password: \$password){
            username
          }
        }
    """;

    createAccountContent = [
      Input(
        hint: 'Username', 
        iconData: Ionicons.person_outline,
        inputController: _registerUsernameController,
        keyboardType: TextInputType.text,
        type: InputType.text,
      ),
      Input(
        hint: 'Email', 
        iconData: Ionicons.mail_outline,
        inputController: _registerEmailController,
        keyboardType: TextInputType.emailAddress,
        type: InputType.text,
      ),
      Input(
        hint: 'Password', 
        iconData: Ionicons.lock_closed_outline,
        inputController: _registerPasswordController,
        keyboardType: TextInputType.visiblePassword,
        type: InputType.password,
      ),
      Mutation(
        options: MutationOptions(
          document: gql(createUser),
          onCompleted: (dynamic resultData) async{

            final localStorage = await SharedPreferences.getInstance();
            await localStorage.setString('username', resultData['createUser']['user']['username']);
            
            if(!mounted) return;
            
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const WelcomeScreen(),
              ),
            );
          },
        ),
        builder: (RunMutation runMutation, QueryResult? result) {
          return Button(
            text: 'Sign Up', 
            action: () => {

              if(_registerFormKey.currentState!.validate()){
                runMutation({
                  'username': _registerUsernameController.text,
                  'email': _registerEmailController.text,
                  'password': _registerPasswordController.text,
                })
              }
            },
            color: kSecondaryColor,  
          );
        },
      ),
      Visibility(
        visible: _keyboard_toggling,
        child: const OrDivider()
      ),
      Visibility(
        visible: _keyboard_toggling,
        child: const Logos()
      ),
    ];

    loginContent = [
      Input(
        hint: 'Username', 
        iconData: Ionicons.person_outline,
        inputController: _loginUsernameController,
        keyboardType: TextInputType.text,
        type: InputType.text,
      ),
      Input(
        hint: 'Password', 
        iconData: Ionicons.lock_closed_outline,
        inputController: _loginPasswordController,
        keyboardType: TextInputType.visiblePassword,
        type: InputType.password,
      ),
      Mutation(
        options: MutationOptions(
          document: gql(logUser),
          onCompleted: (dynamic resultData) async {

            if(resultData['logUser'] != null){

              final localStorage = await SharedPreferences.getInstance();
              await localStorage.setString('username', resultData['logUser']['username']);
              
              if(!mounted) return;
              
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (context) => const WelcomeScreen(),
                ),
              );

            }else{
              showDialog(
                context: context, 
                builder: (context) => AlertDialog(
                  title: const Text('Error'),
                  content: const Text('Invalid username or password'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.of(context).pop(), 
                      child: const Text('Ok')
                    )
                  ],
              ));
            }
          },
        ),
        builder: (RunMutation runMutation, QueryResult? result) {
          return Button(
            text: 'Log In', 
            action: () => {

              if(_loginFormKey.currentState!.validate()){
                runMutation({
                  'username': _loginUsernameController.text,
                  'password': _loginPasswordController.text,
                })
              }
            },
            color: kSecondaryColor, 
          );
        },
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
        Visibility(
          visible: _keyboard_toggling,
          child: const Positioned(
            top: 136,
            left: 24,
            child: TopText()
          ),
        ),
        Padding(
          padding: const EdgeInsets.only(top: 100),
          child: FocusScope(
            child: Focus(
              onFocusChange: (hasFocus) {
                setState(() {
                  _keyboard_toggling = !hasFocus;
                });
              },
              child: Stack(
                children: [
                  Form(
                    key: _registerFormKey,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: createAccountContent,
                    ),
                  ),
                  Form(
                    key: _loginFormKey,
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: loginContent,
                    ),
                  ),
                ]
              ),
            ),
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