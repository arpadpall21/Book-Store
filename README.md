# Book-Store Backend Service
## Description
- This is a book store backend service with real-life-like features
- A database adapter class is used to simulate the database, on startup dummy books are automatically generated and stored
- The main goal of this project is to use fastAPI tools, so some of the implementations are not optimal (ex: dependency injection usage lead to code duplication which not that professional)

- Clients can:
  - browse through available books
  - order books
  - have their own profile in the store
  - can log out and delete their profile
- Administrators can:
  - monitor book orders in real-time (through ws connection)

## FastAPI Features
- Once the user creates its profile and logged in, he/she receives a session id, this session id is used for all further requests (until logout)
- Route parameters are used by `/store/book/<title>` and `/archive/book/<title>` endpoints
- Query parameters are used by `/store/books?<...>` and `/archive/books?<...>` endpoints
- All request/response data is validated
- All routes are documented via OpenAPI (available on `/docs` or `/redoc` endpoints)
- FastAPI background tasks are used to send emails to users (simulated email service)
- There are 2 storages, a store and an archive, FastAPI dependency injection technique is used to inject one dependency for both endpoints
- Cookies are used for authentication (session id)
- FastAPI middleware is used to log all successful profile requests
- FastAPI decoder is used to jsonify data stored in the database
- FastAPI setup & teardown is used to simulate database connection/disconnection
- Websocket connection is used to broadcast book orders to all connected administrators (administrators are required to have valid credentials to connect)
- Testing the profile endpoints via FastAPI test client

## Setup
- Python version `3.11.4`
- Run `pip install -r requirements.txt` to install required packages (I recommend using a virtual environment)
- Run `fastapi server:app --port 3000` to start the server
- In separate terminal(s) run `python admin_monitor.py` to start administrator book order monitoring (several administrators can be connected)

## Usage
- You will need a REST client to interact with the server (like Postman)
- Request the `http://localhost:3000/<route>` endpoints with the below examples
- Administrator(s) will receive real-time notification when a user orders a book (Administrators also need credentials to connect (credentials are included in websocket admin client `admin_monitor.py`))
- To run tests run `python -m pytest`

### User Profile Request Examples
- Create a new profile (endpoint: `POST http://localhost:3000/profile/create`)
  - Body
```
  {
    "email": "some@email.com",
    "password": "dummyPassword",
  }
```
- Login to an existing profile (endpoint: `POST http://localhost:3000/profile/login`)
  - Will respond with a session id (cookie) that must be sent with all further requests (with Postman this is handled automatically)
  - Body
```
  {
    "email": "some@email.com",
    "password": "dummyPassword",
  }
```
- Logout from a profile (endpoint: `GET http://localhost:3000/profile/logout`)
  - The user must be logged in
  - Session id (cookie) must be sent with the request
- Delete user profile (endpoint: `DELETE http://localhost:3000/profile/delete`)
  - The user must be logged in
  - Session id (cookie) must be sent with the request

### Browse and Order Book Request Examples
**Requirement:** 

-> The User must be logged in and the session id (cookie) must be sent with the request (with Postman this is handled automatically)  

-> Both the `store` and `archive`, endpoints have the same functionality (the below examples are for the `store` endpoint but would work for the `archive` endpoint as well)
- Request all available books (endpoint: `GET http://localhost:3000/store/books`)
- Request the first 100 available books (endpoint: `GET http://localhost:3000/store/books?limit=100`)
- Request the second 100 available books (endpoint: `GET http://localhost:3000/store/books?skip=100&limit=100`)
- Request a specific book (endpoint: `GET http://localhost:3000/store/book/<title>`)
  - for `<tiltle>` (book tile) spaces must be replaced with `_` (ex: `The Great Gatsby` -> `The_Great_Gatsby`)
- Order a book (endpoint: `GET http://localhost:3000/store/order_book/<title>`)
  - for `<tiltle>` (book tile) spaces must be replaced with `_` (ex: `The Great Gatsby` -> `The_Great_Gatsby`)
