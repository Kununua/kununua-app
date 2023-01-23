import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:draggable_home/draggable_home.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class ProductDetails extends StatelessWidget {
  
  final ImageProvider productImage;
  final String productName;
  
  const ProductDetails({
    super.key,
    required this.productImage,
    required this.productName,
  });

  Future<Map<String, dynamic>> _getProduct() async{

    Map<String, dynamic> product = {};

    final MutationOptions getProductByIdOptions = MutationOptions(
      document: gql(getProductById),
      variables: const <String, dynamic>{
        'id': 1,
      },
    );

    final productResult = await globals.client.value.mutate(getProductByIdOptions);

    if (productResult.hasException) {
      product['exception'] = "Ha ocurrido un error. Por favor, inténtelo de nuevo.";
    }else{
      product['name'] = productResult.data!['getProductById']['name'];
      product['image'] = _getImage(productResult.data!['getProductById']['image']);
    }

    return product;
  }

  ImageProvider _getImage(encodedImage){
    return MemoryImage(base64Decode(encodedImage));
  }

  @override
  Widget build(BuildContext context) {

    return FutureBuilder(
      future: _getProduct(),
      builder: (context, productResult) {

        if(productResult.hasData){

          Map<String, dynamic> product = productResult.data!;

          if (product['exception'] != null) {
            return Scaffold(
              appBar: const MainPageAppBar(),
              body: Container(
                height: double.infinity,
                width: double.infinity,
                color: Colors.white,
                child: const Center(
                  child: Text(
                    "Ha ocurrido un error. Por favor, inténtelo de nuevo.",
                    textAlign: TextAlign.center,
                    style: TextStyle(
                      color: Colors.black,
                      fontSize: 20,
                    ),
                  )
                )
              ),
            );
          }else{

            return DraggableHome(
              leading: const Icon(Icons.arrow_back_ios),
              title: Text(productName),
              appBarColor: kPrimaryColor,
              alwaysShowTitle: false,
              backgroundColor: Colors.white,
              curvedBodyRadius: 40,
              // fullyStretchable: true,
              alwaysShowLeadingAndAction: true,
              headerWidget: Image(
                image: product['image'],
                fit: BoxFit.contain,
              ),
              // expandedBody: const CameraPreview(),
              body: [
                Center(
                  child: Text(
                    product['name'],
                    style: const TextStyle(
                      color: Colors.black,
                      fontSize: 20,
                    ),
                  ),
                ),
              ]
            );
          }
        }else{
          return const Center(
            child: CircularProgressIndicator(),
          );
        }
      }
    );
  }
}