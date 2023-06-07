import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_cell.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/utils/globals.dart' as globals;
import 'package:kununua_app/widgets/kununua_grid.dart';
import 'dart:async';

class SearchPage extends StatefulWidget {
  final List<dynamic> productsList;
  final Function updateFilters;
  final int totalResults;
  const SearchPage(
      {super.key,
      required this.updateFilters,
      required this.productsList,
      required this.totalResults});

  @override
  State<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends State<SearchPage> {
  Map<String, List<String>> _filters = {};
  Map<String, List<String>> _filtersSetted = {};
  Map<String, List<String>> _filtersOriginal = {};
  List<Map<String, List<dynamic>>> _productsList = [];
  String _query = "";
  final inputController = TextEditingController();
  Timer? _debounce;
  int pageNumber = 1;
  int limit = 10;
  final controller = ScrollController();

  @override
  void dispose() {
    inputController.dispose();
    _debounce?.cancel();
    super.dispose();
  }

  @override
  void initState() {
    _filters = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': [],
    };
    super.initState();

    controller.addListener(() {
      if (controller.position.maxScrollExtent == controller.offset) {
        pageNumber = pageNumber + 1;

        fetchProducts(_query, pageNumber, limit);
      }
    });
  }

  Future<void> fetchProducts(
      String queryParam, int pageNumberParam, int limitParam) async {
    final QueryOptions getProducts = QueryOptions(
      document: gql(getProductsByName),
      variables: <String, dynamic>{
        'name': queryParam,
        'pageNumber': pageNumberParam,
        'limit': limitParam
      },
    );

    final productsResult = await globals.client.value.query(getProducts);

    var resultList = HelperFunctions.deserializeData(productsResult);
    var productsList = resultList['products'];
    var filtersList = resultList['filters'];

    for (var filter in filtersList) {
      List<String> options = [];
      for (var option in List.from(filter['options'])) {
        options.add(option);
      }
      _filters[filter['key']] = options;
    }
    _filtersSetted = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': [],
    };
    _filtersOriginal = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': [],
      'Nombres': [queryParam],
    };
    widget.updateFilters([...widget.productsList, ...productsList], _filters,
        _filtersSetted, _filtersOriginal);

    setState(() {
      _query = queryParam;
    });
  }

  void _onSearchChanged(String query) {
    if (_debounce?.isActive ?? false) _debounce!.cancel();
    _debounce = Timer(const Duration(milliseconds: 1000), () async {
      if (query.trim().isEmpty) {
        _productsList = [];
        pageNumber = 1;
        _filters = {
          'Supermercados': [],
          'Precio': [],
          'Puntuación': [],
          'Categorías': [],
          'Marcas': [],
        };
        _filtersSetted = {
          'Supermercados': [],
          'Precio': [],
          'Puntuación': [],
          'Categorías': [],
          'Marcas': [],
        };
        _filtersOriginal = {
          'Supermercados': [],
          'Precio': [],
          'Puntuación': [],
          'Categorías': [],
          'Marcas': [],
          'Nombres': [],
        };
        widget.updateFilters(
            _productsList, _filters, _filtersSetted, _filtersOriginal);
        return;
      }

      pageNumber = 1;

      await fetchProducts(query, pageNumber, limit);
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
        controller: controller,
        child: Flex(direction: Axis.vertical, children: [
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
              child: TextField(
                  onChanged: _onSearchChanged,
                  decoration: const InputDecoration(
                      hintText: "Busca cualquier producto",
                      icon: Icon(Icons.search),
                      border: InputBorder.none),
                  style: const TextStyle(
                      backgroundColor: Colors.white,
                      decoration: TextDecoration.none))),
          Flex(
            direction: Axis.vertical,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Text(
                      "Mostrando ${widget.totalResults} resultado${widget.totalResults != 1 ? "s" : ""}"),
                  Button(
                    text: "Filtros",
                    action: () => {Scaffold.of(context).openEndDrawer()},
                    color: kPrimaryColor,
                    paddingContainer: EdgeInsets.zero,
                    paddingButton: const EdgeInsets.fromLTRB(10, 10, 15, 10),
                    icon: const Icon(Icons.filter_alt),
                  )
                ],
              )
            ],
          ),
          (widget.productsList.isNotEmpty)
              ? KununuaGrid(
                  scrollable: true,
                  gridMargin: const EdgeInsets.fromLTRB(20, 10, 20, 10),
                  mainAxisSpacing: 10,
                  crossAxisCount: 2,
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                      ...widget.productsList.map<Widget>((product) {
                        Map<String, dynamic> priceToShow =
                            product['priceSet'][0];

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
                    ])
              : (inputController.text.isNotEmpty)
                  ? const Center(
                      child: CircularProgressIndicator(),
                    )
                  : Container(),
        ]));
  }
}
