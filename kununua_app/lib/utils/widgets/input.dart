import 'package:flutter/material.dart';

class Input extends StatefulWidget {

  final String hint;
  final IconData iconData;
  final TextEditingController inputController;

  const Input({
    super.key,
    required this.hint,
    required this.iconData,
    required this.inputController,
  });

  @override
  State<Input> createState() => _InputState();
}

class _InputState extends State<Input> {
  
  @override
  void dispose() {
    widget.inputController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
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
              controller: widget.inputController,
              textAlignVertical: TextAlignVertical.bottom,
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: BorderSide.none
                ),
                filled: true,
                fillColor: Colors.white,
                hintText: widget.hint,
                prefixIcon: Icon(widget.iconData)
              ),
            ),
          ),
        ),
      );
  }
}