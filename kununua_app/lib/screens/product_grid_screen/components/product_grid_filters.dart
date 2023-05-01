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

class ProductGridFilters extends StatelessWidget {
  final Map<String, List<String>> filters;
  final Function updateProductsList;
  final Map<String, List<String>> settedFilters;
  final Map<String, List<String>> originalFilters;

  const ProductGridFilters(
      {super.key,
      this.filters = const {
        'Supermercados': [],
        'Precio': [],
        'Puntuación': [],
        'Categorías': [],
        'Marcas': []
      },
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

  void updateNamedSettedFilters(key, name, value) {
    if (settedFilters[key]!.contains(name)) {
      if (!value) {
        settedFilters[key]!.remove(name);
      }
    } else {
      if (value) {
        settedFilters[key]!.add(name);
      }
    }
  }

  void updateRangedSettedFilters(key, start, end, min, max) {
    final List<String> range = [
      start.toString(),
      end.toString(),
      min.toString(),
      max.toString()
    ];
    if (settedFilters[key]! != range) {
      settedFilters[key] = range;
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
      supermarkets = [...originalFilters['Supermercados']!];
      supermarkets!.addAll(settedFilters['Supermercados']!);
      if (supermarkets!.isEmpty) {
        supermarkets = null;
      }
      categories = [...originalFilters['Categorías']!];
      categories!.addAll(settedFilters['Categorías']!);
      if (categories!.isEmpty) {
        categories = null;
      }
      brands = [...originalFilters['Marcas']!];
      brands!.addAll(settedFilters['Marcas']!);
      if (brands!.isEmpty) {
        brands = null;
      }

      if (settedFilters['Precio']!.isNotEmpty) {
        minPrice = double.parse(settedFilters['Precio']![0]);
        maxPrice = double.parse(settedFilters['Precio']![1]);
      } else if (originalFilters['Precio']!.isNotEmpty) {
        minPrice = double.parse(originalFilters['Precio']![0]);
        maxPrice = double.parse(originalFilters['Precio']![1]);
      }

      if (settedFilters['Puntuación']!.isNotEmpty) {
        minRating = double.parse(settedFilters['Puntuación']![0]);
        maxRating = double.parse(settedFilters['Puntuación']![1]);
      } else if (originalFilters['Puntuación']!.isNotEmpty) {
        minRating = double.parse(originalFilters['Puntuación']![0]);
        maxRating = double.parse(originalFilters['Puntuación']![1]);
      }

      if (originalFilters['Nombres']!.isNotEmpty) {
        name = originalFilters['Nombres']!.first;
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

      updateProductsList(productsList, settedFilters);
    }

    return Drawer(
        child: ListView.builder(
            itemCount: filters.length + 1,
            itemBuilder: (BuildContext context, int index) {
              if (index == 0) {
                String key = filters.keys.elementAt(index);
                return Column(children: [
                  Padding(
                      padding:
                          const EdgeInsets.only(left: 15, bottom: 10, top: 10),
                      child: Center(
                          child: Text(
                        "Filtra por".toUpperCase(),
                        style: const TextStyle(
                            fontSize: 20, fontWeight: FontWeight.bold),
                      ))),
                  ExpansionTile(
                    title: ProductGridFiltersTitle(name: key),
                    children: [
                      filters[key]!.isEmpty
                          ? const Padding(
                              padding: EdgeInsets.only(bottom: 15),
                              child: Text("No hay parámetros para filtrar",
                                  style:
                                      TextStyle(fontStyle: FontStyle.italic)))
                          : key == "Precio" || key == "Puntuación"
                              ? ProductGridFiltersRange(
                                  start: double.parse(
                                      settedFilters[key]!.isEmpty
                                          ? filters[key]![0]
                                          : settedFilters[key]![0]),
                                  end: double.parse(settedFilters[key]!.isEmpty
                                      ? filters[key]![1]
                                      : settedFilters[key]![1]),
                                  min: double.parse(settedFilters[key]!.isEmpty
                                      ? filters[key]![2]
                                      : settedFilters[key]![2]),
                                  max: double.parse(settedFilters[key]!.isEmpty
                                      ? filters[key]![3]
                                      : settedFilters[key]![3]),
                                  keyName: key,
                                  updateRangedSettedFilters:
                                      updateRangedSettedFilters)
                              : ListView.builder(
                                  itemCount: filters[key]!.length,
                                  shrinkWrap: true,
                                  itemBuilder:
                                      (BuildContext context, int index) {
                                    return ProductGridFiltersElement(
                                        name: filters[key]![index],
                                        isChecked: settedFilters[key]!
                                                .contains(filters[key]![index])
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
              if (index == filters.length) {
                bool hasFilters = false;
                filters.forEach((key, value) {
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
                        paddingContainer: const EdgeInsets.only(top: 10),
                        paddingButton:
                            const EdgeInsets.fromLTRB(20, 10, 20, 10),
                        //icon: const Icon(Icons.filter_alt)
                      )
                    ]);
              }
              String key = filters.keys.elementAt(index);
              return ExpansionTile(
                title: ProductGridFiltersTitle(name: key),
                children: [
                  filters[key]!.isEmpty
                      ? const Padding(
                          padding: EdgeInsets.only(bottom: 15),
                          child: Text("No hay parámetros para filtrar",
                              style: TextStyle(fontStyle: FontStyle.italic)))
                      : key == "Precio" || key == "Puntuación"
                          ? ProductGridFiltersRange(
                              start: double.parse(settedFilters[key]!.isEmpty
                                  ? filters[key]![0]
                                  : settedFilters[key]![0]),
                              end: double.parse(settedFilters[key]!.isEmpty
                                  ? filters[key]![1]
                                  : settedFilters[key]![1]),
                              min: double.parse(settedFilters[key]!.isEmpty
                                  ? filters[key]![2]
                                  : settedFilters[key]![2]),
                              max: double.parse(settedFilters[key]!.isEmpty
                                  ? filters[key]![3]
                                  : settedFilters[key]![3]),
                              keyName: key,
                              updateRangedSettedFilters:
                                  updateRangedSettedFilters)
                          : ListView.builder(
                              itemCount: filters[key]!.length,
                              shrinkWrap: true,
                              itemBuilder: (BuildContext context, int index) {
                                return ProductGridFiltersElement(
                                    name: filters[key]![index],
                                    isChecked: settedFilters[key]!
                                            .contains(filters[key]![index])
                                        ? true
                                        : false,
                                    keyName: key,
                                    updateNamedSettedFilters:
                                        updateNamedSettedFilters);
                              })
                ],
              );
            }));
  }
}
