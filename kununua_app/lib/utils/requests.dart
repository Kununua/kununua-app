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
      }
    }
    """;

/* ------------------------------- PRODUCT RETRIEVAL ------------------------------- */

String getProductById = """
    query getProductById(\$id: Int!){
      getProductById(id: \$id){
        id
        name
        price
        unitPrice
        url
        isVegetarian
        isGlutenFree
        isFreezed
        isFromCountry
    		isEco
    		isWithoutSugar
    		isWithoutLactose
        image
        supermarket{
          name
          mainUrl
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
    """;

String getProductsByCategory = """
    query getProductsByCategory(\$categoryName: String!){
      getProductsByCategory(category: \$categoryName){
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
  query getProductsWithOffer{
  getProductsWithOffer{
    id
    name
    price
    unitPrice
    url
    isVegetarian
    isGlutenFree
    isFreezed
    isFromCountry
    isEco
    isWithoutSugar
    isWithoutLactose
    image
    supermarket{
      name
      mainUrl
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
""";

String getProductsByName = """
    query getProductsByName(\$name: String!){
      getProductsByName(name: \$name){
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
        product{
          id
          name
          supermarket{
            name
          }
          price
          unitPrice
          image
        }
      }
    }

""";

String addToCart = """

    mutation addEntryToCart(\$userToken: String!, \$productId: Int!, \$amount: Int!){
      addEntryToCart(userToken: \$userToken, productId: \$productId, amount: \$amount){
        entry{
          quantity
          product{
            name
          }
        }
      }
    }

""";

String editCartEntry = """

    mutation editCartEntry(\$userToken: String!, \$productId: Int!, \$amount: Int!){
      editCartEntry(userToken: \$userToken, productId: \$productId, amount: \$amount){
        entry{
          quantity
          product{
            name
          }
        }
      }
    }

""";
