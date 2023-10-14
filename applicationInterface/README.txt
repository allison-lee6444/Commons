WARNING: The current code is not set up yet to interact with the database as the database is not yet complete.  See the commented out code.  It is currently functioning only with the test database.  It has not been tested with the student database.

First, run the file authenticationService.py which is located in the same directory as this file.  To interact with the server, use the following paths and pass the following parameters.

Sample API calls were made with fetch API on the front-end during testing.

API Methods:
  - authenticateUserSignIn
    - Use: Authenticate user sign in attempts.
    - Path: [SERVER]/authenticateUserSignIn/[USERNAME_DATA]?password=[PASSWORD_DATA]
    - Parameters: Username, Password

  - registerNewUser
    - Use: Register new users.
    - Path: [SERVER]/registerNewUser/[USERNAME_DATA]?password=[PASSWORD_DATA]
    - Parameters: Username, Password

