

import 'package:flutter/material.dart';

class KununuaConfirm extends StatelessWidget {

  final String title;
  final String text;
  final String confirmationText;
  final String cancelText;
  final VoidCallback onConfirm;
  final VoidCallback onCancel;


  const KununuaConfirm({
    super.key,
    this.title = '',
    this.text = '',
    this.confirmationText = 'Cancelar',
    this.cancelText = 'Continuar',
    required this.onConfirm,
    required this.onCancel,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(title),
      content: Text(text),
      actions: [
        TextButton(
          onPressed: onCancel,
          child: const Text('Cancelar'),
        ),
        TextButton(
          onPressed: onConfirm,
          child: const Text('Continuar'),
        ),
      ],
    );
  }
}

void showDialogWidget(BuildContext context, Widget confirmationWidget) {
  showDialog(
    context: context,
    builder: (context) => confirmationWidget
  );
}