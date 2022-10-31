import 'package:flutter/material.dart';

enum InputType{
  text,
  password,
  email
}
class Input extends StatefulWidget {

  final String hint;
  final IconData iconData;
  final TextEditingController inputController;
  final TextInputType keyboardType;
  final InputType type;

  const Input({
    super.key,
    required this.hint,
    required this.iconData,
    required this.inputController,
    required this.keyboardType,
    required this.type,
  });

  @override
  State<Input> createState() => _InputState();
}

class _InputState extends State<Input> {

  late bool _obscureText;
  
  @override
  void initState() { 
    _obscureText = false;
    super.initState();
  }

  @override
  void dispose() {
    widget.inputController.dispose();
    super.dispose();
  }

  String? _validateInput(String? value){
    if(value == null || value.isEmpty){
      return 'Please enter some text';
    }
    return null;

    //widget.type == InputType.email ? (value) => value!.contains('@') ? value.split("@")[1].contains(".") ? null: 'Invalid email' : 'Invalid email' : null,
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: const EdgeInsets.symmetric(horizontal: 36, vertical: 8),
        child: SizedBox(
          child: Material(
            elevation: 8,
            shadowColor: Colors.black87,
            color: Colors.transparent,
            borderRadius: BorderRadius.circular(30),
            child: TextFormField(
              controller: widget.inputController,
              textAlignVertical: TextAlignVertical.center,
              keyboardType: widget.keyboardType,
              obscureText: widget.type == InputType.password ? !_obscureText : false,
              validator: _validateInput,
              decoration: InputDecoration(
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(30),
                  borderSide: BorderSide.none
                ),
                filled: true,
                fillColor: Colors.white,
                hintText: widget.hint,
                prefixIcon: Icon(widget.iconData),
                suffixIcon: widget.type == InputType.password ? IconButton(
                  icon: Icon(_obscureText ? Icons.visibility : Icons.visibility_off),
                  onPressed: () => setState(() => _obscureText = !_obscureText),
                ) : null,
              ),
            ),
          ),
        ),
      );
  }
}