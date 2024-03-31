This project consists of 2 files, 1 is an HTML file and another is a python file.
The html file is used as a basic registration page UI and the python file is used to create a local API server.
The workflow looks like this
UI -> user enters registration details -> user submits the worklfow -> the POST API call is invoked -> if the data is already present in the database, the data is not injected -> if the data is new, the data is injected into the database.

This project assumes that a PostgreSQL database is already installed in the system, any other users using this will need to update the database credentials in the python file

The purpose of this project is to enable users who are newly any type of automation to have an idea of a basic end to end application (UI, API, DB)
