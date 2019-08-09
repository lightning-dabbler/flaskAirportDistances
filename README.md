Airport Distance Calculator
============
> A web app that calculates the distance between two U.S. airports in nautical miles.

> Featured with Autocompletion functionality and Google maps plotting.

Installation
--------
* The version of Python I used is 3.6.3

- install flask
- install flask-googlemaps
- install wtforms
```
pip install flask
pip install flask-googlemaps
pip install wtforms
```

NfdcFacilities.xls is the data I got from the [Federal Aviation Administration].

It was then converted to a csv formatted file and was used to create a database with ```sqlite3```

The code for the database set up is within airportDatabaseSetUp.ipynb and the database (airport.db) resides within the database subdirectory of airportDistanceLookUp

The app is flaskAirport.py
- Run the app
```
python flaskAirport.py
```

The app will be running on http://127.0.0.1:5000/ or http://localhost:5000/

Sample Image of Results
---------
### *Calculated Distance between JFK and GUM*
<img src="./sampleImages/JFK-GUM.png" alt="Calculated Distance between JFK and GUM">

Tech 
------
* [flask]
* [wtforms]
* [flask-googlemaps]
* [Jinja2]
* [Google Maps Javascript API]
* [jQuery]

Author
--------
* Osarodion Irabor

License
-------
MIT

[Federal Aviation Administration]: https://www.faa.gov/airports/airport_safety/airportdata_5010/
[flask]: http://flask.pocoo.org/
[flask-googlemaps]: https://github.com/rochacbruno/Flask-GoogleMaps
[wtforms]: https://github.com/wtforms/wtforms
[Google Maps Javascript API]: https://developers.google.com/maps/documentation/javascript/tutorial
[Jinja2]: http://jinja.pocoo.org/docs/2.10/
[jQuery]: https://api.jquery.com/
