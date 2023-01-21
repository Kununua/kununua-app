import 'package:flutter/material.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:draggable_home/draggable_home.dart';

class ProductDetails extends StatelessWidget {
  
  final ImageProvider productImage;
  final String productName;
  
  const ProductDetails({
    super.key,
    required this.productImage,
    required this.productName,
  });

  @override
  Widget build(BuildContext context) {

    return DraggableHome(
      leading: const Icon(Icons.arrow_back_ios),
      title: Text(productName),
      appBarColor: kPrimaryColor,
      alwaysShowTitle: false,
      backgroundColor: Colors.white,
      curvedBodyRadius: 40,
      // fullyStretchable: true,
      alwaysShowLeadingAndAction: true,
      headerWidget: Container(
        color: Colors.grey,
        child: Image(
          image: productImage,
          fit: BoxFit.cover,
        ),
      ),
      // expandedBody: const CameraPreview(),
      body: const [
        Center(
          child:Text(
            "Esto es una prueba",
            style: TextStyle(
              color: Colors.black,
              fontSize: 20,
            ),
          ),
        ),
      ]
    );
  }
}