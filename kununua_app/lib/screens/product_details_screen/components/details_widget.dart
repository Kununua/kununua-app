import 'dart:io';

import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/screens/product_details_screen/components/draggable_home.dart';

class DetailsWidget extends StatelessWidget {
  
  final Map<String, dynamic> product;
  
  const DetailsWidget({
    super.key,
    required this.product,
  });

  @override
  Widget build(BuildContext context) {
    return DraggableHome(
              leading: Platform.isIOS ? const Icon(Icons.arrow_back_ios) : const Icon(Icons.arrow_back),
              title: Container(),
              appBarColor: kPrimaryColor,
              alwaysShowTitle: false,
              backgroundColor: Color.fromARGB(255, 231, 231, 231),
              shadowBorder: true,
              curvedBodyRadius: 40,
              // fullyStretchable: true,
              alwaysShowLeadingAndAction: true,
              headerWidget: Container(
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
                            image: product['image'],
                            fit: BoxFit.contain,
                          ),
                        ),
                      ),
                    ),
                  ]
                ),
              ),
              // expandedBody: const CameraPreview(),
              body: [
                Padding(
                  padding: const EdgeInsets.only(left: 20, right: 20),
                  child: Flex(
                    direction: Axis.horizontal,
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        product['name'],
                        style: const TextStyle(
                          color: Colors.black,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const Text(
                        "10.00",
                        style: TextStyle(
                          color: Colors.black,
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ]
                  ),
                ),
              ]
            );
  }
}