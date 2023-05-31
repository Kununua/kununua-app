import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/pages/list_page/components/list_extended_view.dart';
import 'package:kununua_app/pages/list_page/list_page.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/widgets/kununua_confirm.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';
import 'package:intl/intl.dart';

class ListPreview extends StatelessWidget {
  const ListPreview({
    super.key,
    required this.date,
    required this.products,
  });

  final List<Object?> products;
  final String date;

  @override
  Widget build(BuildContext context) {
    DateTime parsedDate = DateTime.parse(date);
    double containerHeight = 100;
    double iconSize = 25;
    double iconPositionTop = (containerHeight / 2) - (iconSize / 2);

    return InkWell(
      onTap: () {
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) =>
                ListExtendedView(title: 'Lista 1', products: products),
          ),
        );
      },
      child: Stack(children: [
        Container(
            margin: const EdgeInsets.only(left: 10, right: 10),
            height: containerHeight,
            decoration: const BoxDecoration(
              border: Border(
                bottom: BorderSide(
                  color: Colors.grey,
                  width: 2,
                ),
              ),
            ),
            child: Row(children: [
              Expanded(
                  child: Container(
                      padding: const EdgeInsets.all(10),
                      child: Column(
                          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Lista 1',
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                fontSize: 20,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            Text(
                              "Creada el ${DateFormat("dd/MM/yyyy").format(parsedDate)} a las ${DateFormat("HH:mm").format(parsedDate)}",
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                fontSize: 15,
                                fontWeight: FontWeight.w300,
                              ),
                            ),
                          ])))
            ])),
        Positioned(
            right: 25,
            top: iconPositionTop,
            child: MouseRegion(
              cursor: SystemMouseCursors.click,
              child: GestureDetector(
                onTap: () {},
                child: Icon(Icons.arrow_forward_ios,
                    color: kPrimaryColor, size: iconSize),
              ),
            ))
      ]),
    );
  }
}
