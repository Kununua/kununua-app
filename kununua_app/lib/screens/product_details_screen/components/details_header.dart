import 'package:flutter/material.dart';

class DetailsHeader extends StatelessWidget {
  
  final ImageProvider productImage;
  
  const DetailsHeader({
    super.key,
    required this.productImage,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
                width: double.infinity,
                color: Colors.white,
                child: Stack(
                  children: [
                    Container(
                      height: double.infinity,
                      color: Colors.white,
                    ),
                    Center(
                      child: SizedBox(
                        height: MediaQuery.of(context).size.height * 0.3,
                        child: AspectRatio(
                          aspectRatio: 16/9,
                          child: Image(
                            image: productImage,
                            fit: BoxFit.contain,
                          ),
                        ),
                      ),
                    ),
                  ]
                ),
              );
  }
}