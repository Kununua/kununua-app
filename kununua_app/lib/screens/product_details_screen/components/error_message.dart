import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/common_app_bar.dart';

class ErrorMessage extends StatelessWidget {

  final String message;

  const ErrorMessage({
    super.key,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
              appBar: const CommonAppBar(
                text: 'Error',
              ),
              body: Container(
                height: double.infinity,
                width: double.infinity,
                color: Colors.white,
                child: Center(
                  child: Text(
                    message,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Colors.black,
                      fontSize: 20,
                    ),
                  )
                )
              ),
            );
  }
}