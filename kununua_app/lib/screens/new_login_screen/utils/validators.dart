String? nameValidator(String? value){
  return _nameSurnameValidator(value, 'Nombre');
}

String? surnameValidator(String? value){
  return _nameSurnameValidator(value, 'Apellidos');
}

String? _nameSurnameValidator(String? value, String type){
  if (value == null || value.isEmpty) {
    return 'Este campo es obligatorio';
  }else if(value.length < 3 && value.length >= 50){
    if (value == "Nombre") return 'El nombre debe tener entre 3 y 50 caracteres';
    return 'Los apellidos deben tener entre 3 y 50 caracteres';
  }
  return null;
}