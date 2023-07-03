import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class KununuaConfirm extends StatelessWidget {
  final String title;
  final String text;
  final String confirmationText;
  final String cancelText;
  final bool isDestructive;
  final VoidCallback onConfirm;
  final VoidCallback onCancel;

  const KununuaConfirm({
    super.key,
    this.title = '',
    this.text = '',
    this.confirmationText = 'Continuar',
    this.cancelText = 'Cancelar',
    this.isDestructive = false,
    required this.onConfirm,
    required this.onCancel,
  });

  @override
  Widget build(BuildContext context) {
    if (Theme.of(context).platform == TargetPlatform.iOS) {
      return CupertinoAlertDialog(
        title: Text(
          title,
          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
        ),
        content: Text(text),
        actions: [
          CupertinoDialogAction(
            onPressed: onCancel,
            child: Text(cancelText),
          ),
          CupertinoDialogAction(
            onPressed: onConfirm,
            child: Text(confirmationText,
                style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: isDestructive ? Colors.red : Colors.blue)),
          ),
        ],
      );
    } else {
      return AlertDialog(
        title: Text(title,
            style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
        content: Text(text),
        actions: [
          TextButton(
            onPressed: onCancel,
            child: Text(cancelText),
          ),
          TextButton(
            onPressed: onConfirm,
            child: Text(confirmationText,
                style: TextStyle(
                    fontWeight: FontWeight.bold,
                    color: isDestructive ? Colors.red : Colors.blue)),
          ),
        ],
      );
    }
  }
}

void showDialogWidget(BuildContext context, Widget confirmationWidget) {
  if (Theme.of(context).platform == TargetPlatform.iOS) {
    showCupertinoDialog(
        context: context, builder: (context) => confirmationWidget);
  } else {
    showDialog(context: context, builder: (context) => confirmationWidget);
  }
}
