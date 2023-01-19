String logUser = """
       query logUser(\$username: String!, \$password: String!){
          logUser(username: \$username, password: \$password){
            username
          }
        }
    """;