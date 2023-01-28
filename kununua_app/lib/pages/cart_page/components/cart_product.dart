import 'package:flutter/material.dart';
import 'package:kununua_app/utils/extensions/string_extension.dart';

class CartProduct extends StatefulWidget {
  
  final Map<String, dynamic> product;
  final int quantity;
  final bool topBorder;
  final bool bottomBorder;

  const CartProduct({
    super.key,
    required this.product,
    required this.quantity,
    this.topBorder = false,
    this.bottomBorder = false,
  });

  @override
  State<CartProduct> createState() => _CartProductState();
}

class _CartProductState extends State<CartProduct> {

  late int amount;

  @override
  void initState() {
    super.initState();
    amount = widget.quantity;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(left: 10),
      height: 125,
      decoration: BoxDecoration(
        border: Border(
          top: BorderSide(
            color: widget.topBorder ? Colors.grey : Colors.transparent,
            width: 2,
          ),
          bottom: BorderSide(
            color: widget.bottomBorder ? Colors.grey : Colors.transparent,
            width: 2,
          ),
        ),
      ),
      child: Row(
        children: [
          Image(
            image: widget.product['imageEncoded'],
            width: 100,
            height: 100,
            fit: BoxFit.cover
          ),
          Expanded(
            child: Container(
              padding: const EdgeInsets.all(10),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    (widget.product["name"] as String).capitalizeFirstOfEach(),
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(
                    widget.product["supermarket"]['name'],
                    style: const TextStyle(
                      fontSize: 15,
                      fontWeight: FontWeight.w300,
                    ),
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        "${widget.product["price"]} €",
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      Row(
                        children: [
                          IconButton(
                            onPressed: () {
                              setState(() {
                                if (amount > 1){
                                  amount--;
                                }
                              });
                            },
                            icon: const Icon(Icons.remove),
                          ),
                          Text(
                            amount.toString(),
                            style: const TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          IconButton(
                            onPressed: () {
                              setState(() {
                                amount++;
                              });
                            },
                            icon: const Icon(Icons.add),
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
    );
  }
}