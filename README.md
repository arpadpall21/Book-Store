  - Library API 
      - user must login (simple username and password -> gets back a session cookie)
        - this session cookie must be sent with every request (validation)

      - 2 stores (books & old books)
      - for the sake of simplicity, no password check




  My shiny new FastAPI project!
      - implements:
        - the 4 famous http methods
                    - user login-update-delete-get_info  / logout / get / post / put / delete
        - validations and documentation (document that are available on /docs)
                    - pay attention on development
        - has query string 
                    - when getting all books
        - has path parameters
                    - when getting a specific book
        - cookie (authentication)
                    - included in all requests
        - custom response code (like 201 / 404 -> documentation)
                    - when creating a new profile / getting a book that is not exist
        - raise http exception
                    - when getting a book that is not exist
        - dependency injection
                    - use this to bridge books and old books
        - decoder
                    - store the book dates as python date (this guy will be used to decode that)
        - middleware
                    - to log every request
        - at least on test
                    - login / logout / get_info / update / delete profile
        - a router
                    - authentication router (for login / logout / get_info / update / delete)
        - websocket for monitoring
                    - live monitoring when the user reserves a book
        - background task
                    - email sending (simulate a 5 second delay for sending email)
        - setup and teardown
                    - for db fake db simulation -> this will be great
