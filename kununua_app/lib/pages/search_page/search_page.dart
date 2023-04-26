import 'package:flutter/material.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/widgets/button.dart';

class SearchPage extends StatelessWidget {
  final int totalResults = 0;
  const SearchPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Flex(direction: Axis.vertical, children: [
      Container(
          margin: const EdgeInsets.all(10),
          padding: const EdgeInsets.fromLTRB(5, 0, 10, 0),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            border: const Border(
              top: BorderSide(color: Colors.grey, width: 2),
              bottom: BorderSide(
                color: Colors.grey,
                width: 2,
              ),
              left: BorderSide(
                color: Colors.grey,
                width: 2,
              ),
              right: BorderSide(
                color: Colors.grey,
                width: 2,
              ),
            ),
          ),
          child: const TextField(
              decoration: InputDecoration(
                  hintText: "Busca cualquier producto",
                  icon: Icon(Icons.search),
                  border: InputBorder.none),
              style: TextStyle(
                  backgroundColor: Colors.white,
                  decoration: TextDecoration.none))),
      Flex(
        direction: Axis.vertical,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text(
                  "Mostrando $totalResults resultado${totalResults != 1 ? "s" : ""}"),
              Button(
                text: "Filtros",
                action: () => {Scaffold.of(context).openEndDrawer()},
                color: kPrimaryColor,
                paddingContainer: EdgeInsets.zero,
                paddingButton: const EdgeInsets.fromLTRB(10, 10, 15, 10),
                icon: const Icon(Icons.filter_alt),
              )
            ],
          ),
        ],
      )
    ]);
  }
}
