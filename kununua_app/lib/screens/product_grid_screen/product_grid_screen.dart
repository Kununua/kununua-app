import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/app_bars/common_app_bar.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_cell.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/widgets/kununua_grid.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class ProductGridScreen extends StatefulWidget {
  final String category;
  final int supermarketId;
  final String supermarketName;
  final bool isSupermarket;

  const ProductGridScreen(
      {super.key,
      this.category = "",
      this.supermarketId = 0,
      this.supermarketName = "",
      this.isSupermarket = false});

  @override
  State<ProductGridScreen> createState() => _ProductGridScreenState();
}

class _ProductGridScreenState extends State<ProductGridScreen> {
  late final Future getProductsFuture;
  final controller = ScrollController();
  Map<String, List<String>> _filtersSetted = {};
  Map<String, List<String>> _originalFilters = {};
  List<dynamic> _productsList = [];
  bool _hasBeenUpdated = false;
  int pageNumber = 1;
  int limit = 10;

  @override
  void initState() {
    _filtersSetted = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': []
    };
    _originalFilters = widget.isSupermarket
        ? {
            'Supermercados': [widget.supermarketName],
            'Precio': [],
            'Puntuación': [],
            'Categorías': [],
            'Marcas': [],
            'Nombres': [],
          }
        : {
            'Supermercados': [],
            'Precio': [],
            'Puntuación': [],
            'Categorías': [widget.category],
            'Marcas': [],
            'Nombres': [],
          };
    _productsList = [];
    _hasBeenUpdated = false;
    super.initState();

    getProductsFuture = widget.isSupermarket
        ? _getProductsBySupermarket(pageNumber, limit)
        : _getProductsByCategory(pageNumber, limit);

    controller.addListener(() {
      if (controller.position.maxScrollExtent == controller.offset) {
        pageNumber = pageNumber + 1;
        if (widget.isSupermarket) {
          _getProductsBySupermarket(pageNumber, limit);
        } else {
          _getProductsByCategory(pageNumber, limit);
        }
      }
    });
  }

  void updateProductsList(
      List<dynamic> productsList, Map<String, List<String>> filtersSetted) {
    setState(() {
      _productsList = productsList;
      _filtersSetted = filtersSetted;
      _hasBeenUpdated = true;
    });
  }

  Future<void> _getProductsByCategory(
      int pageNumberParam, int limitParam) async {
    final MutationOptions getProducts = MutationOptions(
      document: gql(getProductsByCategory),
      variables: <String, dynamic>{
        'categoryName': widget.category,
        'pageNumber': pageNumberParam,
        'limit': limitParam
      },
    );

    final productsResult = await globals.client.value.mutate(getProducts);
    var productsList = HelperFunctions.deserializeListData(productsResult);

    setState(() {
      if (!_hasBeenUpdated) {
        _productsList = [..._productsList, ...productsList];
      }
    });
  }

  Future<void> _getProductsBySupermarket(
      int pageNumberParam, int limitParam) async {
    final QueryOptions getProducts = QueryOptions(
      document: gql(getProductsBySupermarket),
      variables: <String, dynamic>{
        'supermarketId': widget.supermarketId,
        'pageNumber': pageNumberParam,
        'limit': limitParam
      },
    );

    final productsResult = await globals.client.value.query(getProducts);

    if (productsResult.hasException) {
      debugPrint(productsResult.exception.toString());
    }

    var productsList = HelperFunctions.deserializeListData(productsResult);

    setState(() {
      if (!_hasBeenUpdated) {
        _productsList = [..._productsList, ...productsList];
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: ProductGridFilters(
        updateProductsList: updateProductsList,
        settedFilters: _filtersSetted,
        originalFilters: _originalFilters,
      ),
      appBar: CommonAppBar(
        text: widget.isSupermarket ? widget.supermarketName : widget.category,
      ),
      body: Container(
        color: kBackgroundColor,
        child: FutureBuilder(
          future: getProductsFuture,
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            if (_productsList.isNotEmpty) {
              return KununuaGrid(
                  scrollable: true,
                  scrollController: controller,
                  gridMargin: const EdgeInsets.fromLTRB(20, 10, 20, 10),
                  mainAxisSpacing: 10,
                  crossAxisCount: 2,
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ..._productsList.map<Widget>((product) {
                      Map<String, dynamic> priceToShow = widget.isSupermarket
                          ? (product['priceSet'] as List)
                              .where((price) =>
                                  price['supermarket']['name'] ==
                                  widget.supermarketName)
                              .toList()[0] as Map<String, dynamic>
                          : product['priceSet'][0];
                      String productCurrency = priceToShow['supermarket']
                              ['country']['currency']['symbol'] ??
                          priceToShow['supermarket']['country']['currency']
                              ['code'];
                      return ProductGridCell(
                        id: int.parse(product['id']),
                        image: product['image'],
                        title: product['name'],
                        price: priceToShow['price'],
                        offerPrice: '',
                        weight: "${priceToShow['weight']}",
                        currency: productCurrency,
                      );
                    }).toList(),
                    ...[const CircularProgressIndicator()]
                  ]);
            } else {
              return const Center(
                child: CircularProgressIndicator(),
              );
            }
          },
        ),
      ),
    );
  }
}
