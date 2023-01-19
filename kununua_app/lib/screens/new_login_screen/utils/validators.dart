String? nameValidator(String? value){
  return _nameSurnameValidator(value, 'Nombre');
}

String? surnameValidator(String? value){
  return _nameSurnameValidator(value, 'Apellidos');
}

String? _nameSurnameValidator(String? value, String type){
  if (value == null || value.isEmpty) {
    return 'Este campo es obligatorio';
  }else if(value.length < 3){
    return '$type demasiado corto${type == "Apellidos" ? "s" : ""}';
  }
  return null;
}