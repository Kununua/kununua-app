import 'dart:io';

import 'package:flutter/material.dart';
import 'package:kununua_app/app_bars/main_page_app_bar.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:draggable_home/draggable_home.dart';

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
}