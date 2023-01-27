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

String verifyToken = """
    mutation verifyToken(\$token: String!){
      verifyToken(token: \$token){
        payload
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
        offerPrice
        unitOfferPrice
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