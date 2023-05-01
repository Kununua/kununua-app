import 'package:flutter/material.dart';
import 'package:blurrycontainer/blurrycontainer.dart';
import 'package:animations/animations.dart';
import 'package:kununua_app/screens/product_grid_screen/product_grid_screen.dart';
import 'package:kununua_app/utils/constants.dart';

class MainPageCategoryCell extends StatelessWidget {
  
  final String categoryName;
  final ImageProvider categoryImage;
  final bool isLoading;


  const MainPageCategoryCell({
    super.key,
    this.categoryName = '',
    this.categoryImage = const AssetImage(''),
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {

    if(isLoading){
      return Container(
              margin: const EdgeInsets.fromLTRB(10, 0, 10, 0),
              height: 150,
              width: 150,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(20),
                boxShadow: const [
                  BoxShadow(
                    offset: Offset(0, 17),
                    blurRadius: 10,
                    spreadRadius: -13,
                    color: Colors.black,
                  ),
                ],
              ),
              child: const Center(
                child: CircularProgressIndicator(),
              )
            );
    }else{
      return OpenContainer(
        transitionType: ContainerTransitionType.fade,
        transitionDuration: const Duration(milliseconds: 500),
        closedColor: kBackgroundColor,
        closedElevation: 0,
        clipBehavior: Clip.none,
        closedBuilder: (context, openContainer) {
          return Container(
                  margin: const EdgeInsets.fromLTRB(10, 0, 10, 0),
                  height: 150,
                  width: 150,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                    boxShadow: const [
                      BoxShadow(
                        offset: Offset(0, 17),
                        blurRadius: 10,
                        spreadRadius: -13,
                        color: Colors.black,
                      ),
                    ],
                  ),
                  child: Stack(
                    children: [
                  ClipRRect(
                      borderRadius: BorderRadius.circular(8.0),
                      child: Image(
                        image: categoryImage,
                        fit: BoxFit.cover,
                        height: 150,
                      )),
                      Center(
                        child: BlurryContainer(
                          padding: const EdgeInsets.fromLTRB(10, 5, 10, 5),
                          color: const Color.fromARGB(118, 255, 255, 255),
                          blur: 5,
                          borderRadius: const BorderRadius.all(Radius.circular(10)),
                          child: Text(
                            categoryName,
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.bold,
                              ),
                            )
                        )
                      )
                    ],
                  )
                );
        },
        openBuilder: (context, action) {
          return ProductGridScreen(category: categoryName);
        },
        onClosed: (_) {},
      );
    }
  }
}