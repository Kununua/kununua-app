import 'package:flutter/material.dart';
import 'package:kununua_app/screens/product_details_screen/components/details_widget.dart';
import 'package:kununua_app/screens/product_details_screen/components/error_message.dart';
import 'package:kununua_app/screens/product_details_screen/components/loading_widget.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/utils/helper_functions.dart';

class ProductDetails extends StatefulWidget {
  final int productId;
  final Map<String, dynamic> product;
  
  const ProductDetails({
    super.key,
    this.productId = 0,
    this.product = const {},
  });

  @override
  State<ProductDetails> createState() => _ProductDetailsState();
}

class _ProductDetailsState extends State<ProductDetails> {

  late final Future getProductFuture;

  Future<Map<String, dynamic>> _getProduct() async{

    Map<String, dynamic> product = {};

    final MutationOptions getProductByIdOptions = MutationOptions(
      document: gql(getProductById),
      variables: <String, dynamic>{
        'id': widget.productId,
      },
    );

    final productResult = await globals.client.value.mutate(getProductByIdOptions);

    if (productResult.hasException) {
      product['exception'] = "Ha ocurrido un error. Por favor, inténtelo de nuevo.";
    }else{
      product = HelperFunctions.deserializeData(productResult);
    }

    return product;
  }

  @override
  void initState() {
    super.initState();
    getProductFuture = _getProduct();
  }

  @override
  Widget build(BuildContext context) {

    if(widget.product.isNotEmpty){
      return DetailsWidget(product: widget.product);
    }else{
      return FutureBuilder(
        future: getProductFuture,
        builder: (context, productResult) {

          if(productResult.hasData){

            Map<String, dynamic> product = productResult.data!;

            if (product['exception'] != null) {
              return ErrorMessage(message: product['exception']);
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
}