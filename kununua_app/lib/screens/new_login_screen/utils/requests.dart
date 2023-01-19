/* ------------------------------- USER CREDENTIALS ------------------------------- */

String logUser = """
       query logUser(\$username: String!, \$password: String!){
          logUser(username: \$username, password: \$password){
            username
          }
        }
    """;

String tokenAuth = """
    mutation tokenAuth(\$username: String!, \$password: String!){
      tokenAuth(username: \$username, password: \$password){
        token
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