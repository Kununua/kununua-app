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

  const ProductGridScreen({super.key, required this.category});

  @override
  State<ProductGridScreen> createState() => _ProductGridScreenState();
}

class _ProductGridScreenState extends State<ProductGridScreen> {
  Map<String, List<String>> _filters = {};
  Map<String, List<String>> _filtersSetted = {};
  Map<String, List<String>> _originalFilters = {};
  List<Map<String, dynamic>> _productsList = [];
  bool _hasBeenUpdated = false;

  @override
  void initState() {
    _filters = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': []
    };
    _filtersSetted = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': []
    };
    _originalFilters = {
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
  }

  void updateProductsList(List<Map<String, dynamic>> productsList,
      Map<String, List<String>> filtersSetted) {
    setState(() {
      _productsList = productsList;
      _filtersSetted = filtersSetted;
      _hasBeenUpdated = true;
    });
  }

  Future<List<Map<String, dynamic>>> _getProductsByCategory() async {
    final MutationOptions getProducts = MutationOptions(
      document: gql(getProductsByCategory),
      variables: <String, dynamic>{'categoryName': widget.category},
    );

    final productsResult = await globals.client.value.mutate(getProducts);
    var productsList = HelperFunctions.deserializeListData(productsResult,
        otherOperationName: 'products');
    var filtersList = HelperFunctions.deserializeListData(productsResult,
        otherOperationName: 'filters');

    for (var filter in filtersList) {
      List<String> options = [];
      for (var option in List.from(filter['options'])) {
        options.add(option);
      }
      _filters[filter['key']] = options;
    }

    setState(() {
      if (!_hasBeenUpdated) {
        _filters = _filters;
        _productsList = productsList;
      }
    });

    return productsList;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      endDrawer: ProductGridFilters(
        filters: _filters,
        updateProductsList: updateProductsList,
        settedFilters: _filtersSetted,
        originalFilters: _originalFilters,
      ),
      appBar: CommonAppBar(
        text: widget.category,
      ),
      body: Container(
        color: kBackgroundColor,
        child: FutureBuilder(
          future: _getProductsByCategory(),
          builder: (BuildContext context, AsyncSnapshot snapshot) {
            if (_productsList.isNotEmpty) {
              return KununuaGrid(
                  scrollable: true,
                  gridMargin: const EdgeInsets.fromLTRB(20, 10, 20, 10),
                  mainAxisSpacing: 10,
                  crossAxisCount: 2,
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: _productsList
                      .map<Widget>((product) => ProductGridCell(
                            id: int.parse(product['id']),
                            image: product['image'],
                            title: product['name'],
                            price: product['priceSet'][0]['price'],
                            offerPrice: '',
                            unitPrice: '',
                            weightUnit: product['weightUnit'] ?? '',
                            currency: product['priceSet'][0]['supermarket']
                                    ['country']['currency']['symbol'] ??
                                product['priceSet'][0]['supermarket']['country']
                                    ['currency']['code'],
                          ))
                      .toList());
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
