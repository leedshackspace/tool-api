# tool-api
An 'API'/web interface for administering machines & users.

# requirements
See "requirements.txt" for exact versions
- Python3
- Peewee (version greater than V3 - I am running V3.0.16)
- Flask
- PyMySQL
- A MySQL server

# how to run
The app is currently in development mode. To run,`python3 run.py` will start a server that listens on 0.0.0.0:5000 which will allow hardware to connect to the API.

# database
The database has been dumped under the folder "db_dump" - this contains some test data that was used during development, and the database schema.

The file "models.py" will need to be changed to have the correct database connection string.

# how do JSON?
Currently, the only endpoint that will return json is `/canuse/<machineuid>/<cardid>`

The format this expects is a GET request to the above URL, with the machine UID and card ID. This will return a JSON array with the format of `[{"canuse": 0, "caninduct": 0}]` which will change depending on the permissions of the user.

I plan on adding functionality to allow other endpoints to return JSON in the future, this is being developed on the `/machines` endpoint - if a GET request is made with a Accept header of `application/json` this will eventually return a JSON response.
