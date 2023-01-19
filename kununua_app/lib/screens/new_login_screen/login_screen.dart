import 'dart:math' as math;
import 'package:flutter/material.dart';
import 'package:flutter_login/flutter_login.dart';
import 'package:ionicons/ionicons.dart';
import 'package:kununua_app/screens/welcome_screen/welcome_screen.dart';
import 'package:kununua_app/screens/new_login_screen/components/center_widget/center_widget.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/screens/new_login_screen/utils/validators.dart';
import 'package:kununua_app/screens/new_login_screen/utils/requests.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/new_login_screen/utils/globals.dart' as globals;

class LoginScreen extends StatelessWidget {

  const LoginScreen({
    super.key,
  });

  Duration get loginTime => const Duration(milliseconds: 0);

  Future<String?> _authUser(LoginData data) async {

    debugPrint('Name: ${data.name}, Password: ${data.password}');

    final MutationOptions options = MutationOptions(
      document: gql(logUser),
      variables: <String, dynamic>{
        'username': data.name,
        'password': data.password,
      },
    );

    final result = await globals.client.value.mutate(options);

    if (result.data?['logUser'] == null) {
      return 'Invalid credentials';
    }
    return null;
  }

  Future<String?> _signupUser(SignupData data) {
    debugPrint('Signup Name: ${data.name}, Password: ${data.password}');
    return Future.delayed(loginTime).then((_) {
      return null;
    });
  }

  Future<String?> _recoverPassword(String name) {
    //TODO: implement recovery password
    debugPrint('Name: $name');
    return Future.delayed(loginTime).then((_) {
      // if (!users.containsKey(name)) {
      //   return 'User not exists';
      // }
      return null;
    });
  }

  Widget topWidget(double screenWidth){
    return Transform.rotate(
      angle: -35 * math.pi / 180,
      child: Container(
        width: 1.2 * screenWidth,
        height: 1.2 * screenWidth,
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(150),
          gradient: const LinearGradient(
            begin: Alignment(-0.2, -0.8),
            end: Alignment.bottomCenter,
            colors: [
              Color(0x007CBFCF),
              Color(0xB316BFC4),
            ],
          ),
          ),
        )
      );
  }

  Widget bottomWidget(double screenWith){
    return Container(
      width: 1.5 * screenWith,
      height: 1.5 * screenWith,
      decoration: const BoxDecoration(
        shape: BoxShape.circle,
        gradient: LinearGradient(
          begin: Alignment(0.6, -1.1),
          end: Alignment(0.7, 0.8),
          colors: [
            Color(0xDB4BE8CC),
            Color(0x005CDBCF),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final screenSize = MediaQuery.of(context).size;

    return Stack(
      children: [
        Container(
          width: screenSize.width,
          height: screenSize.height,
          decoration: const BoxDecoration(
            color: kBackgroundColor
          ),
        ),
        Positioned(
          top: -160,
          left: -30,
          child: topWidget(screenSize.width),
        ),
        Positioned(
          bottom: -180,
          left: -40,
          child: bottomWidget(screenSize.width)
        ),
        CenterWidget(size: screenSize),
        FlutterLogin(
          title: 'KUNUNUA',
          theme: LoginTheme(
            titleStyle: const TextStyle(
              color: Colors.white,
              fontFamily: 'Montserrat',
              fontWeight: FontWeight.w600,
              fontSize: 40,
            ),
            accentColor: Colors.white,
            buttonTheme: const LoginButtonTheme(
              backgroundColor: kSecondaryColor,
            ),
            pageColorLight: Colors.transparent,
            pageColorDark: Colors.transparent,
            authButtonPadding: const EdgeInsets.fromLTRB(0, 20, 0, 10),
            cardInitialHeight: 400,
          ),
          logo: const AssetImage('assets/images/google.png'),
          userType: LoginUserType.name,
          onLogin: _authUser,
          onSignup: _signupUser,
          loginProviders: <LoginProvider>[
            LoginProvider(
              button: Buttons.googleDark,
              label: 'Google',
              callback: () async {
                debugPrint('start google sign in');
                await Future.delayed(loginTime);
                debugPrint('stop google sign in');              
                return null;
              },
            ),
            LoginProvider(
              button: Buttons.facebook,
              label: 'Facebook',
              callback: () async {            
                debugPrint('start facebook sign in');
                await Future.delayed(loginTime);
                debugPrint('stop facebook sign in');              
                return null;
              },
            ),
            LoginProvider(
              button: Buttons.appleDark,
              label: 'Apple',
              callback: () async {            
                debugPrint('start facebook sign in');
                await Future.delayed(loginTime);
                debugPrint('stop facebook sign in');              
                return null;
              },
            ),
          ],
          onSubmitAnimationCompleted: () {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => const WelcomeScreen(),
              ),
            );
          },
          onRecoverPassword: _recoverPassword,
          additionalSignupFields: [
            const UserFormField(
              keyName: 'Nombre',
              icon: Icon(Ionicons.person),
              fieldValidator: nameValidator,
              userType: LoginUserType.name
            ),
            const UserFormField(
              keyName: 'Apellidos',
              icon: Icon(Ionicons.person),
              fieldValidator: surnameValidator,
              userType: LoginUserType.name
            ),
            UserFormField(
              keyName: 'Email',
              icon: const Icon(Ionicons.mail),
              fieldValidator: (value) {
                if (value == null || value.isEmpty || !value.contains('@') || !value.contains('.')) {
                  return 'Este campo debe contener un email válido';
                }
                return null;
              },
              userType: LoginUserType.email,
            ),
          ],
          userValidator: (value) {

            int valueLength = value != null ? value.length : 0;

            if (valueLength == 0){
              return "ESte campo es obligatorio";
            }else if (valueLength < 6 && valueLength > 25) {
              return "El usuario debe tener entre 6 y 24 caracteres";
            }
            return null;
          },
          passwordValidator: (value) {
            int valueLength = value != null ? value.length : 0;

            if (valueLength == 0){
              return "Este campo es obligatorio";
            }else if (valueLength < 6) {
              return "La contraseña debe tener al menos 6 caracteres";
            }
            return null;
          },
          messages: LoginMessages(
            userHint: 'Usuario',
            passwordHint: 'Contraseña',
            confirmPasswordHint: 'Confirmar contraseña',
            loginButton: 'INICIAR SESIÓN',
            signupButton: 'CREAR CUENTA',
            forgotPasswordButton: '¿Olvidaste tu contraseña?',
            flushbarTitleSuccess: 'Listo',
            flushbarTitleError: 'Error',
            recoverPasswordButton: 'RECUPERAR CONTRASEÑA',
            goBackButton: 'VOLVER',
            confirmPasswordError: '¡Las contraseñas no coinciden!',
            recoverPasswordIntro: 'Recupera tu contraseña',
            recoverPasswordDescription: 'Se enviará un correo electrónico a la direccion asociada a este usuario para recuperar la contraseña',
            recoverPasswordSuccess: 'Se acaba de enviar un email para restablecer la contraseña. Por favor, revisa tu bandeja de entrada.',
            providersTitleFirst: 'o inicia sesión con',
            additionalSignUpFormDescription: 'Por favor, completa los siguientes campos para terminar de crear tu cuenta',
            additionalSignUpSubmitButton: 'CREAR CUENTA',
            signUpSuccess: '¡Cuenta creada con éxito!',
          ),
          termsOfService: [
            TermOfService(
              id: 'general-term',
              mandatory: true,
              text: 'Acepto los términos y condiciones del servicio',
              validationErrorMessage: 'Debe aceptar este campo',
              linkUrl: 'https://www.google.com',
            ),
          ],
      ),]
    );
  }
}