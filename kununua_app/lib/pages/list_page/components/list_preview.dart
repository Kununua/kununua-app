import 'package:flutter/cupertino.dart';
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
    required this.id,
    required this.title,
    required this.date,
    required this.products,
    required this.removeItem,
  });

  final int id;
  final String title;
  final List<dynamic> products;
  final String date;
  final Function removeItem;

  Future<bool> promptUser(
      BuildContext context, DismissDirection direction) async {
    if (Theme.of(context).platform == TargetPlatform.iOS) {
      return await showCupertinoDialog<bool>(
            context: context,
            builder: (context) => KununuaConfirm(
              onConfirm: () {
                Navigator.of(context).pop(true);
              },
              onCancel: () {
                Navigator.of(context).pop(false);
              },
              text:
                  "¿Estás seguro de que quieres eliminar la lista $title ? Esta acción es irreversible.",
              title: "Eliminar lista",
              confirmationText: 'Eliminar',
              isDestructive: true,
            ),
          ) ??
          false;
    } else {
      return await showDialog<bool>(
            context: context,
            builder: (context) => KununuaConfirm(
              onConfirm: () {
                Navigator.of(context).pop(true);
              },
              onCancel: () {
                Navigator.of(context).pop(false);
              },
              text:
                  "¿Estás seguro de que quieres eliminar la lista $title ? Esta acción es irreversible.",
              title: "Eliminar lista",
              confirmationText: 'Eliminar',
              isDestructive: true,
            ),
          ) ??
          false;
    }
  }

  Future<bool> deleteListMutation() async {
    final MutationOptions deleteListMutation = MutationOptions(
      document: gql(deleteList),
      variables: <String, dynamic>{
        'userToken': globals.prefs!.getString('jwtToken'),
        'listId': id,
      },
    );

    final deleteListResult =
        await globals.client.value.mutate(deleteListMutation);

    if (deleteListResult.hasException) {
      return false;
    }

    return true;
  }

  @override
  Widget build(BuildContext context) {
    DateTime parsedDate = DateTime.parse(date).toLocal();
    double containerHeight = 100;
    double iconSize = 25;
    double iconPositionTop = (containerHeight / 2) - (iconSize / 2);

    return InkWell(
        onTap: () {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) =>
                  ListExtendedView(title: title, products: products),
            ),
          );
        },
        child: Dismissible(
          key: Key('List Preview $id'),
          direction: DismissDirection.endToStart,
          background: Container(
              color: Colors.red,
              alignment: Alignment.centerRight,
              padding: const EdgeInsets.only(right: 20.0),
              child: const Icon(
                Icons.delete,
                color: Colors.white,
                size: 40,
              )),
          confirmDismiss: (direction) => promptUser(context, direction),
          onDismissed: (direction) async {
            removeItem();
            bool isRemoved = await deleteListMutation();
            if (isRemoved && context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content:
                      Text('La lista $title ha sido eliminada correctamente')));
            } else if (context.mounted) {
              ScaffoldMessenger.of(context).showSnackBar(SnackBar(
                  content: Text(
                      'Ha ocurrido un error al eliminar la lista $title y no ha podido completarse la acción')));
            }
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
                                  title,
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
        ));
  }
}
