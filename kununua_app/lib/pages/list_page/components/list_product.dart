import 'dart:ffi';

import 'package:animations/animations.dart';
import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/main_screen.dart';
import 'package:kununua_app/screens/product_details_screen/product_details_screen.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/widgets/kununua_confirm.dart';
import 'package:kununua_app/widgets/kununua_nav_bar/kununua_nav_bar.dart';
import 'package:kununua_app/keys.dart';
import 'dart:async';

class ListProduct extends StatefulWidget {
  final Map<String, dynamic> product;
  final int quantity;
  final bool isCrossed;
  final int id;

  const ListProduct({
    super.key,
    required this.product,
    required this.quantity,
    required this.isCrossed,
    required this.id,
  });

  @override
  State<ListProduct> createState() => _ListProductState();
}

class _ListProductState extends State<ListProduct> {
  bool _isCrossed = false;
  Timer? _debounce;

  @override
  void initState() {
    _isCrossed = widget.isCrossed;
    super.initState();
  }

  @override
  void dispose() {
    _debounce?.cancel();
    super.dispose();
  }

  void crossElement() {
    setState(() {
      _isCrossed = !_isCrossed;
    });
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 1500), () async {
      final MutationOptions crossProductOptions = MutationOptions(
        document: gql(crossCartEntry),
        variables: <String, dynamic>{
          'userToken': globals.prefs!.getString('jwtToken'),
          'cartEntryId': widget.id,
          'isCrossed': _isCrossed,
        },
      );

      final crossResult =
          await globals.client.value.mutate(crossProductOptions);

      if (crossResult.hasException) {
        setState(() {
          _isCrossed = !_isCrossed;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(children: [
      InkWell(
        onLongPress: crossElement,
        child: Container(
          margin: const EdgeInsets.only(left: 10, right: 10),
          height: 125,
          decoration: const BoxDecoration(
            border: Border(
              bottom: BorderSide(
                color: Colors.grey,
                width: 2,
              ),
            ),
          ),
          child: Row(
            children: [
              OpenContainer(
                  transitionType: ContainerTransitionType.fade,
                  transitionDuration: const Duration(milliseconds: 500),
                  closedColor: kBackgroundColor,
                  closedElevation: 0,
                  clipBehavior: Clip.none,
                  closedBuilder: (context, openDetails) {
                    if (widget.product['amount'] != null &&
                        widget.product['amount'] > 1) {
                      return ClipRect(
                          child: Banner(
                              message: "PACK",
                              location: BannerLocation.topStart,
                              color: Colors.indigo,
                              child: Image(
                                  image: widget.product['image'],
                                  width: 100,
                                  height: 100,
                                  fit: BoxFit.cover)));
                    } else {
                      return Image(
                          image: widget.product['product']['image'],
                          width: 100,
                          height: 100,
                          fit: BoxFit.cover);
                    }
                  },
                  openBuilder: (context, action) {
                    return ProductDetails(
                        productId: int.parse(widget.product['product']['id']));
                  },
                  onClosed: (_) {}),
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(10),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        (widget.product['product']["name"] as String).title(),
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          decoration: _isCrossed
                              ? TextDecoration.lineThrough
                              : TextDecoration.none,
                          color: _isCrossed ? Colors.grey : null,
                        ),
                      ),
                      Text(
                        widget.product["supermarket"]['name'],
                        style: TextStyle(
                          fontSize: 15,
                          fontWeight: FontWeight.w300,
                          decoration: _isCrossed
                              ? TextDecoration.lineThrough
                              : TextDecoration.none,
                          color: _isCrossed ? Colors.grey : null,
                        ),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text(
                            "${widget.product["price"]} ${widget.product["supermarket"]["country"]["currency"]["symbol"]}",
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                              decoration: _isCrossed
                                  ? TextDecoration.lineThrough
                                  : TextDecoration.none,
                              color: _isCrossed ? Colors.grey : null,
                            ),
                          ),
                          Row(
                            children: [
                              Text(
                                "Cantidad: ${widget.quantity}",
                                style: TextStyle(
                                  fontSize: 15,
                                  fontWeight: FontWeight.w300,
                                  decoration: _isCrossed
                                      ? TextDecoration.lineThrough
                                      : TextDecoration.none,
                                  color: _isCrossed ? Colors.grey : null,
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    ]);
  }
}
