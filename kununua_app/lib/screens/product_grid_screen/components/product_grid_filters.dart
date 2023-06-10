import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters_element.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters_range.dart';
import 'package:kununua_app/screens/product_grid_screen/components/product_grid_filters_title.dart';
import 'package:kununua_app/utils/constants.dart';
import 'package:kununua_app/utils/helper_functions.dart';
import 'package:kununua_app/utils/requests.dart';
import 'package:kununua_app/widgets/button.dart';
import 'package:kununua_app/utils/globals.dart' as globals;

class ProductGridFilters extends StatefulWidget {
  const ProductGridFilters(
      {super.key,
      required this.updateProductsList,
      this.settedFilters = const {
        'Supermercados': [],
        'Precio': [],
        'Puntuación': [],
        'Categorías': [],
        'Marcas': []
      },
      this.originalFilters = const {
        'Supermercados': [],
        'Precio': [],
        'Puntuación': [],
        'Categorías': [],
        'Marcas': [],
        'Nombres': [],
      }});
  final Function updateProductsList;
  final Map<String, List<String>> settedFilters;
  final Map<String, List<String>> originalFilters;

  @override
  State<ProductGridFilters> createState() => _ProductGridFiltersState();
}

class _ProductGridFiltersState extends State<ProductGridFilters> {
  TextEditingController editingController = TextEditingController();
  Map<String, List<String>> dataFiltered = {};
  Map<String, List<String>> _filters = {};
  late bool _dataLoaded;

  final Map<String, List<String>> _filtersEmpty = const {
    'Supermercados': [],
    'Precio': [],
    'Puntuación': [],
    'Categorías': [],
    'Marcas': []
  };

  @override
  void initState() {
    dataFiltered = const {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': []
    };
    _filters = const {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': []
    };
    _dataLoaded = false;
    super.initState();
  }

  @override
  void dispose() {
    editingController.dispose();
    super.dispose();
  }

  void updateNamedSettedFilters(key, name, value) {
    if (widget.settedFilters[key]!.contains(name)) {
      if (!value) {
        widget.settedFilters[key]!.remove(name);
      }
    } else {
      if (value) {
        widget.settedFilters[key]!.add(name);
      }
    }
  }

  void filterSearchResults(String query, String key) {

    Map<String, List<String>> newDataFiltered = {};

    for (var key in _filters.keys) {
      newDataFiltered[key] = [];

      for (var item in _filters[key]!) {
        if (item.toLowerCase().contains(query.toLowerCase().trim())) {
          newDataFiltered[key]!.add(item);
        }
      }
    }

    if (query.trim().isEmpty) {
      setState(() {
        dataFiltered = _filters;
      });
      
      return;
    }

    setState(() {
      dataFiltered = newDataFiltered;
    });
  }

  Future<Map<String, List<String>>> loadFilters() async {
    QueryOptions getFiltersOptions = QueryOptions(
      document: gql(getFilters),
    );
    var filtersResult = await globals.client.value.query(getFiltersOptions);
    var filtersData = HelperFunctions.deserializeListData(filtersResult);
    Map<String, List<String>> filtersMap = {
      'Supermercados': [],
      'Precio': [],
      'Puntuación': [],
      'Categorías': [],
      'Marcas': []
    };
    if (filtersData.isNotEmpty) {
      for (var filter in filtersData) {
        List<String> options = [];
        for (var option in List.from(filter['options'])) {
          options.add(option);
        }
        filtersMap[filter['key']] = options;
      }
    }

    if(!_dataLoaded){
      setState(() {
      _filters = filtersMap;
      dataFiltered = filtersMap;
      _dataLoaded = true;
    }); 
    }

    return filtersMap;
  }

  void updateRangedSettedFilters(key, start, end, min, max) {
    final List<String> range = [
      start.toString(),
      end.toString(),
      min.toString(),
      max.toString()
    ];
    if (widget.settedFilters[key]! != range) {
      widget.settedFilters[key] = range;
    }
  }

  @override
  Widget build(BuildContext context) {
    List<String>? supermarkets = [];
    List<String>? categories = [];
    List<String>? brands = [];
    double? minPrice;
    double? maxPrice;
    double? minRating;
    double? maxRating;
    String? name;
    void applyFilters() async {
      List<Map<String, dynamic>> productsList = [];
      supermarkets = [...widget.originalFilters['Supermercados']!];
      supermarkets!.addAll(widget.settedFilters['Supermercados']!);
      if (supermarkets!.isEmpty) {
        supermarkets = null;
      }
      categories = [...widget.originalFilters['Categorías']!];
      categories!.addAll(widget.settedFilters['Categorías']!);
      if (categories!.isEmpty) {
        categories = null;
      }
      brands = [...widget.originalFilters['Marcas']!];
      brands!.addAll(widget.settedFilters['Marcas']!);
      if (brands!.isEmpty) {
        brands = null;
      }

      if (widget.settedFilters['Precio']!.isNotEmpty) {
        minPrice = double.parse(widget.settedFilters['Precio']![0]);
        maxPrice = double.parse(widget.settedFilters['Precio']![1]);
      } else if (widget.originalFilters['Precio']!.isNotEmpty) {
        minPrice = double.parse(widget.originalFilters['Precio']![0]);
        maxPrice = double.parse(widget.originalFilters['Precio']![1]);
      }

      if (widget.settedFilters['Puntuación']!.isNotEmpty) {
        minRating = double.parse(widget.settedFilters['Puntuación']![0]);
        maxRating = double.parse(widget.settedFilters['Puntuación']![1]);
      } else if (widget.originalFilters['Puntuación']!.isNotEmpty) {
        minRating = double.parse(widget.originalFilters['Puntuación']![0]);
        maxRating = double.parse(widget.originalFilters['Puntuación']![1]);
      }

      if (widget.originalFilters['Nombres']!.isNotEmpty) {
        name = widget.originalFilters['Nombres']!.first;
      }

      final MutationOptions getProducts = MutationOptions(
        document: gql(getProductsFiltered),
        variables: <String, dynamic>{
          'supermarkets': supermarkets,
          'categories': categories,
          'brands': brands,
          'minPrice': minPrice,
          'maxPrice': maxPrice,
          'minRating': minRating,
          'maxRating': maxRating,
          'name': name
        },
      );

      final productsResult = await globals.client.value.mutate(getProducts);

      productsList = HelperFunctions.deserializeListData(productsResult);

      widget.updateProductsList(productsList, widget.settedFilters);
    }

    return Drawer(
        child: FutureBuilder(
            future: loadFilters(),
            builder: (BuildContext context, AsyncSnapshot<dynamic> snapshot) {
              if (snapshot.hasData) {
                return ListView.builder(
                    itemCount: snapshot.data.length + 1,
                    itemBuilder: (BuildContext context, int index) {
                      if (index == 0) {
                        String key = snapshot.data.keys.elementAt(index);
                        return Column(children: [
                          Padding(
                              padding: const EdgeInsets.only(
                                  left: 15, bottom: 10, top: 10),
                              child: Center(
                                  child: Text(
                                "Filtra por".toUpperCase(),
                                style: const TextStyle(
                                    fontSize: 20, fontWeight: FontWeight.bold),
                              ))),
                          ExpansionTile(
                            title: ProductGridFiltersTitle(name: key),
                            children: [
                              _filters[key]!.length < 30
                                  ? Container()
                                  : Padding(
                                      padding: const EdgeInsets.all(15),
                                      child: SizedBox(
                                        height: 50,
                                        width: double.infinity,
                                        child: TextField(
                                          controller: editingController,
                                          onChanged: (value) {
                                            filterSearchResults(value, key);
                                          },
                                          decoration: const InputDecoration(
                                              hintText: "Filtra por nombre",
                                              prefixIcon: Icon(Icons.search),
                                              border: OutlineInputBorder(
                                                  borderRadius:
                                                      BorderRadius.all(
                                                          Radius.circular(
                                                              25.0)))),
                                        ),
                                      ),
                                    ),
                              snapshot.data[key]!.isEmpty
                                  ? const Padding(
                                      padding: EdgeInsets.only(bottom: 15),
                                      child: Text("No hay parámetros para filtrar",
                                          style: TextStyle(
                                              fontStyle: FontStyle.italic)))
                                  : key == "Precio" || key == "Puntuación"
                                      ? ProductGridFiltersRange(
                                          start: double.parse(widget
                                                  .settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![0]
                                              : widget.settedFilters[key]![0]),
                                          end: double.parse(widget.settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![1]
                                              : widget.settedFilters[key]![1]),
                                          min: double.parse(widget.settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![2]
                                              : widget.settedFilters[key]![2]),
                                          max: double.parse(
                                              widget.settedFilters[key]!.isEmpty
                                                  ? snapshot.data[key]![3]
                                                  : widget.settedFilters[key]![3]),
                                          keyName: key,
                                          updateRangedSettedFilters: updateRangedSettedFilters)
                                      : widget.originalFilters[key]!.isEmpty
                                          ? snapshot.data[key]!.length > 30
                                              ? ListView.builder(
                                                  itemCount: dataFiltered[key]!.length,
                                                  shrinkWrap: true,
                                                  itemBuilder: (BuildContext context, int index) {
                                                    return ProductGridFiltersElement(
                                                        name: dataFiltered[
                                                            key]![index],
                                                        isChecked: widget
                                                                .settedFilters[
                                                                    key]!
                                                                .contains(
                                                                    snapshot.data[
                                                                            key]![
                                                                        index])
                                                            ? true
                                                            : false,
                                                        keyName: key,
                                                        updateNamedSettedFilters:
                                                            updateNamedSettedFilters);
                                                  })
                                              : ListView.builder(
                                                  itemCount: snapshot.data[key]!.length,
                                                  shrinkWrap: true,
                                                  itemBuilder: (BuildContext context, int index) {
                                                    return ProductGridFiltersElement(
                                                        name: snapshot
                                                            .data[key]![index],
                                                        isChecked: widget
                                                                .settedFilters[
                                                                    key]!
                                                                .contains(
                                                                    snapshot.data[
                                                                            key]![
                                                                        index])
                                                            ? true
                                                            : false,
                                                        keyName: key,
                                                        updateNamedSettedFilters:
                                                            updateNamedSettedFilters);
                                                  })
                                          : ListView.builder(
                                              itemCount: widget.originalFilters[key]!.length,
                                              shrinkWrap: true,
                                              itemBuilder: (BuildContext context, int index) {
                                                return ProductGridFiltersElement(
                                                    name:
                                                        widget.originalFilters[
                                                            key]![index],
                                                    isChecked: widget
                                                            .settedFilters[key]!
                                                            .contains(widget
                                                                    .originalFilters[
                                                                key]![index])
                                                        ? true
                                                        : false,
                                                    keyName: key,
                                                    updateNamedSettedFilters:
                                                        updateNamedSettedFilters);
                                              })
                            ],
                          )
                        ]);
                      }
                      if (index == snapshot.data.length) {
                        bool hasFilters = false;
                        snapshot.data.forEach((key, value) {
                          if (value.isNotEmpty) {
                            hasFilters = true;
                            return;
                          }
                        });
                        return Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Button(
                                text: "Filtrar productos",
                                action: hasFilters ? applyFilters : null,
                                color: kPrimaryColor,
                                paddingContainer:
                                    const EdgeInsets.only(top: 10),
                                paddingButton:
                                    const EdgeInsets.fromLTRB(20, 10, 20, 10),
                                //icon: const Icon(Icons.filter_alt)
                              )
                            ]);
                      }
                      String key = snapshot.data.keys.elementAt(index);
                      return ExpansionTile(
                        title: ProductGridFiltersTitle(name: key),
                        children: [
                          snapshot.data[key]!.length < 30
                              ? Container()
                              : Padding(
                                  padding: const EdgeInsets.all(15),
                                  child: SizedBox(
                                    height: 50,
                                    width: double.infinity,
                                    child: TextField(
                                      controller: editingController,
                                      onChanged: (value) {
                                        filterSearchResults(value, key);
                                      },
                                      decoration: const InputDecoration(
                                          hintText: "Filtra por nombre",
                                          prefixIcon: Icon(Icons.search),
                                          border: OutlineInputBorder(
                                              borderRadius: BorderRadius.all(
                                                  Radius.circular(25.0)))),
                                    ),
                                  ),
                                ),
                          snapshot.data[key]!.isEmpty
                              ? const Padding(
                                  padding: EdgeInsets.only(bottom: 15),
                                  child: Text("No hay parámetros para filtrar",
                                      style: TextStyle(
                                          fontStyle: FontStyle.italic)))
                              : key == "Precio" || key == "Puntuación"
                                  ? ProductGridFiltersRange(
                                      start: double.parse(
                                          widget.settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![0]
                                              : widget.settedFilters[key]![0]),
                                      end: double.parse(
                                          widget.settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![1]
                                              : widget.settedFilters[key]![1]),
                                      min: double.parse(
                                          widget.settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![2]
                                              : widget.settedFilters[key]![2]),
                                      max: double.parse(
                                          widget.settedFilters[key]!.isEmpty
                                              ? snapshot.data[key]![3]
                                              : widget.settedFilters[key]![3]),
                                      keyName: key,
                                      updateRangedSettedFilters:
                                          updateRangedSettedFilters)
                                  : widget.originalFilters[key]!.isEmpty
                                      ? snapshot.data[key]!.length > 30
                                          ? dataFiltered[key]!.length > 30 
                                          ? ListView.builder(
                                              itemCount: widget.settedFilters[key]!.length,
                                              shrinkWrap: true,
                                              itemBuilder: (BuildContext context, int index) {
                                                return ProductGridFiltersElement(
                                                    name: widget.settedFilters[key]![index],
                                                    isChecked: true,
                                                    keyName: key,
                                                    updateNamedSettedFilters: updateNamedSettedFilters
                                                    );
                                              })
                                              :
                                          ListView.builder(
                                              itemCount: dataFiltered[key]!.length,
                                              shrinkWrap: true,
                                              itemBuilder: (BuildContext context, int index) {
                                                return ProductGridFiltersElement(
                                                    name: dataFiltered[key]![
                                                        index],
                                                    isChecked: widget
                                                            .settedFilters[key]!
                                                            .contains(dataFiltered[key]![index]),
                                                    keyName: key,
                                                    updateNamedSettedFilters:
                                                        updateNamedSettedFilters);
                                              })
                                          : ListView.builder(
                                              itemCount: snapshot.data[key]!.length,
                                              shrinkWrap: true,
                                              itemBuilder: (BuildContext context, int index) {
                                                return ProductGridFiltersElement(
                                                    name: snapshot
                                                        .data[key]![index],
                                                    isChecked: widget
                                                            .settedFilters[key]!
                                                            .contains(snapshot
                                                                    .data[key]![
                                                                index])
                                                        ? true
                                                        : false,
                                                    keyName: key,
                                                    updateNamedSettedFilters:
                                                        updateNamedSettedFilters);
                                              })
                                      : ListView.builder(
                                          itemCount: widget.originalFilters[key]!.length,
                                          shrinkWrap: true,
                                          itemBuilder: (BuildContext context, int index) {
                                            return ProductGridFiltersElement(
                                                name: widget.originalFilters[
                                                    key]![index],
                                                isChecked: widget
                                                        .settedFilters[key]!
                                                        .contains(widget
                                                                .originalFilters[
                                                            key]![index])
                                                    ? true
                                                    : false,
                                                keyName: key,
                                                updateNamedSettedFilters:
                                                    updateNamedSettedFilters);
                                          })
                        ],
                      );
                    });
              }
              return ListView.builder(
                  itemCount: _filtersEmpty.length + 1,
                  itemBuilder: (BuildContext context, int index) {
                    if (index == 0) {
                      String key = _filtersEmpty.keys.elementAt(index);
                      return Column(children: [
                        Padding(
                            padding: const EdgeInsets.only(
                                left: 15, bottom: 10, top: 10),
                            child: Center(
                                child: Text(
                              "Filtra por".toUpperCase(),
                              style: const TextStyle(
                                  fontSize: 20, fontWeight: FontWeight.bold),
                            ))),
                        ExpansionTile(
                          title: ProductGridFiltersTitle(name: key),
                          children: const [
                            Padding(
                                padding: EdgeInsets.only(bottom: 15),
                                child: Text("No hay parámetros para filtrar",
                                    style:
                                        TextStyle(fontStyle: FontStyle.italic)))
                          ],
                        )
                      ]);
                    }
                    if (index == _filtersEmpty.length) {
                      return const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Button(
                              text: "Filtrar productos",
                              action: null,
                              color: kPrimaryColor,
                              paddingContainer: EdgeInsets.only(top: 10),
                              paddingButton:
                                  EdgeInsets.fromLTRB(20, 10, 20, 10),
                              //icon: const Icon(Icons.filter_alt)
                            )
                          ]);
                    }
                    String key = _filtersEmpty.keys.elementAt(index);
                    return ExpansionTile(
                      title: ProductGridFiltersTitle(name: key),
                      children: const [
                        Padding(
                            padding: EdgeInsets.only(bottom: 15),
                            child: Text("No hay parámetros para filtrar",
                                style: TextStyle(fontStyle: FontStyle.italic)))
                      ],
                    );
                  });
            }));
  }
}
