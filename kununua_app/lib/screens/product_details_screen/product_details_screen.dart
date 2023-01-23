import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/screens/product_details_screen/components/details_widget.dart';
import 'package:kununua_app/screens/product_details_screen/components/error_message.dart';
import 'package:kununua_app/screens/product_details_screen/components/loading_widget.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:draggable_home/draggable_home.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class ProductDetails extends StatelessWidget {
  
  final int productId;
  
  const ProductDetails({
    super.key,
    required this.productId,
  });

  Future<Map<String, dynamic>> _getProduct() async{

    Map<String, dynamic> product = {};

    final MutationOptions getProductByIdOptions = MutationOptions(
      document: gql(getProductById),
      variables: <String, dynamic>{
        'id': productId,
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
            return const ErrorMessage(message: "Ha ocurrido un error. Por favor, inténtelo de nuevo.");
          }else{

            return DetailsWidget(product: product);
          }
        }else{
          return const LoadingWidget();
        }
      }
    );
  }
}