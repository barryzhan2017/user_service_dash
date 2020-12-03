# user_service_dash
It uses python dash framework to create user_service-related pages and interact with our server.
* Issue when deploying to elastic beanstalk
    * WSGIPath should be **application**
    * Main file should be called **application.py**
    * Use ```application = app.server``` and ```application.run(debug=True, port=8080)``` to run the server
    * Port should be **8080**
