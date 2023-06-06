/* ------------------------------- USER CREDENTIALS ------------------------------- */

String logUser = """
       mutation tokenAuth(\$username: String!, \$password: String!){
          tokenAuth(username: \$username, password: \$password){
            token
            user{
              username
              firstName
              lastName
              email
              phoneNumber
              profilePicture
              isStaff
            }
          }
        }
    """;

String createUser = """
    mutation createUser(\$username: String!, \$password: String!, \$email: String!, \$firstName: String!, \$lastName: String!){
      createUser(username: \$username, password: \$password, email: \$email, firstName: \$firstName, lastName: \$lastName){
        user{
          username
        }
      }

      tokenAuth(username: \$username, password: \$password){
        token
        user{
          username
          firstName
          lastName
          email
          phoneNumber
          profilePicture
          isStaff
        }
      }

    }
    """;

String createGoogleUser = """

      mutation createGoogleUser(\$accessToken: String!){
        createGoogleUser(accessToken: \$accessToken){
          created
        }
      }
      """;

String refreshToken = """
  mutation refreshToken(\$token: String!){
    refreshToken(token: \$token){
      token
    }
  }
  """;

/* ------------------------------- CATEGORIES RETRIEVAL ------------------------------- */

String getCategories = """
    query getAllCategories{
      getAllCategories{
        name
        image
      }
    }
    """;

/* ------------------------------- PRODUCT RETRIEVAL ------------------------------- */

String getProductById = """
    query getProductById(\$id: Int!){
      getProductById(id: \$id){
        id
        name
        image
        isVegetarian
        isGlutenFree
        isFreezed
        isFromCountry
        isEco
        isWithoutSugar
        isWithoutLactose
        priceSet{
          id
          price
          amount
          weight
          url
          supermarket{
            name
            mainUrl
            image
            country{
              spanishName
              englishName
              code
              phoneCode
              currency{
                name
                code
                symbol
              }
            }
          }
        }
      }
    }
    """;

String getProductsByCategory = """
    query getProductsByCategory(\$categoryName: String!, \$pageNumber: Int, \$limit: Int){
      getProductsByCategory(category: \$categoryName, pageNumber: \$pageNumber, limit: \$limit){
        products {
          id
          name
          image
          priceSet {
            price
            supermarket {
              country {
                currency {
                  code
                  symbol
                }
              }
            }
          }
        }
        filters {
          key
          options
        }
      }
    }
""";

String getOfferProducts = """
  query getProductsWithOffer {
    getProductsWithOffer {
      id
      name
      isVegetarian
      isGlutenFree
      isFreezed
      isFromCountry
      isEco
      isWithoutSugar
      isWithoutLactose
      image
      priceSet {
        price
        url
        supermarket {
          name
          mainUrl
          country {
            spanishName
            englishName
            code
            phoneCode
            currency {
              name
              code
              symbol
            }
          }
        }
      }
    }
  }
""";

String getPacks = """
  query getPacks {
    getPacks {
      id
      name
      isVegetarian
      isGlutenFree
      isFreezed
      isFromCountry
      isEco
      isWithoutSugar
      isWithoutLactose
      image
      priceSet {
        price
        url
        supermarket {
          name
          mainUrl
          country {
            spanishName
            englishName
            code
            phoneCode
            currency {
              name
              code
              symbol
            }
          }
        }
      }
    }
  }
""";

String getProductsByName = """
    query getProductsByName(\$name: String!, \$pageNumber: Int, \$limit: Int){
      getProductsByName(name: \$name, pageNumber: \$pageNumber, limit: \$limit){
        products {
          id
          name
          image
          priceSet {
            price
            supermarket {
              country {
                currency {
                  code
                  symbol
                }
              }
            }
          }
        }
        filters {
          key
          options
        }
      }
    }
""";

String getProductsFiltered = """
    query getProductsFiltered(\$supermarkets: [String], \$categories: [String], \$minPrice: Float, \$maxPrice: Float, \$minRating: Float, \$maxRating: Float, \$brands: [String], \$name: String){
      filterProducts(supermarkets: \$supermarkets, categories: \$categories, minPrice: \$minPrice, maxPrice: \$maxPrice, minRating: \$minRating, maxRating: \$maxRating, brands: \$brands, name: \$name){
        id
        name
        image
        priceSet {
          price
          supermarket {
            country {
              currency {
                code
                symbol
              }
            }
          }
        }
      }
    }
""";

/* ------------------------------- CART ------------------------------- */

String getProductsInCart = """

    query getCart(\$userToken: String!){
      getCart(userToken: \$userToken){
        quantity
        locked
        productPrice{
          id
          price
          product{
            id
            name
            image
          }
          supermarket{
            name
          }
        }
      }
    }

""";

String addToCart = """

    mutation addEntryToCart(\$userToken: String!, \$priceId: Int!, \$amount: Int!){
      addEntryToCart(userToken: \$userToken, priceId: \$priceId, amount: \$amount){
        entry{
          quantity
          productPrice{
            product{
              name
            }
          }
        }
      }
    }

""";

String editCartEntry = """

    mutation editCartEntry(\$userToken: String!, \$priceId: Int!, \$amount: Int, \$locked: Boolean){
      editCartEntry(userToken: \$userToken, priceId: \$priceId, amount: \$amount, locked: \$locked){
        entry{
          quantity
          productPrice{
            product{
              name
            }
          }
        }
      }
    }

""";

String upgradeCart = """

    mutation upgradeCart(\$userToken: String!, \$maxSupermarkets: Int){
      upgradeCart(userToken: \$userToken, maxSupermarkets: \$maxSupermarkets){
        entry{
          quantity
          productPrice{
            product{
              name
            }
          }
        }
      }
    }

""";

/* ------------------------------- LISTS ------------------------------- */

String getLists = """
  query getLists(\$userToken: String!){
    getLists(userToken: \$userToken){
      id
      name
      date
      productentrySet{
        quantity
        productPrice{
          id
          price
          supermarket{
            name
            country{
              currency{
                symbol
              }
            }
          }
          product{
            id
            name
            image
          }
        }
      }
    }
  }
""";

String createList = """
  mutation createList(\$userToken: String!, \$listName: String!){
    createList(userToken: \$userToken, listName: \$listName){
      list{
        id
        name
        date
        productentrySet{
          quantity
          productPrice{
            price
            supermarket{
              name
              country{
                currency{
                  symbol
                }
              }
            }
            product{
              id
              name
              image
            }
          }
        }
      }
    }
  }
""";

String deleteList = """
  mutation deleteList(\$userToken: String!, \$listId: Int!){
    deleteList(userToken: \$userToken, listId: \$listId){
      isDeleted
    }
  }
""";

/* ------------------------------- PRODUCTS VALORATION ------------------------------- */

String addOpinionRequest = """
  mutation addReview(\$userToken: String!, \$productId: Int!, \$rating: Float!){
    addProductRatingMutation(userToken: \$userToken, productId: \$productId, rating: \$rating){
      productRated{
        rating
        user{
          username
        }
        product{
          name
        }
      }
    }
  }
""";