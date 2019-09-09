# Python 3.6.3

import sqlite3
import math
from flask import Flask, render_template, url_for,request, Response,jsonify
from wtforms import TextField, Form
from flask_googlemaps import GoogleMaps,Map
import pytz
from datetime import datetime
app = Flask(__name__) 


app.config['GOOGLEMAPS_KEY'] = "AIzaSyA6BxL9P4U2TIoWiBsch4b6URo8lgpLEQg"
GoogleMaps(app)

DATABASE  =  './database/airport.db'

#Table = Airport
# Columns = ID,LocationID, State, County, City, FacilityName, Latitude,Longitude
def nauticalCalc(lat1,lon1,lat2,lon2):
    lat1 = ((lat1/3600)*math.pi)/180 #Convert secs to degrees then to radians
    lon1 = ((lon1/3600)*math.pi)/180 #Convert secs to degrees then to radians
    lat2 = ((lat2/3600)*math.pi)/180 #Convert secs to degrees then to radians
    lon2 = ((lon2/3600)*math.pi)/180 #Convert secs to degrees then to radians
    R = 3440 #radius of Earth in Nautical Miles
    posA = (R*math.cos(lat1),0,R*math.sin(lat1)) #3D position of first location
    posB = (R*math.cos(lat2)*math.cos(lon2-lon1),R*math.cos(lat2)*math.sin(lon2-lon1),R*math.sin(lat2)) #3D position of second location
    scalarProdLeft = (posA[0]*posB[0]+posA[1]*posB[1]+posA[2]*posB[2])/(R**2)
    #scalarProdRight = math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1)+math.sin(lat1)*math.sin(lat2)
    #return scalarProdLeft,scalarProdRight
    x = math.acos(scalarProdLeft)
    return R*x

def get_airports():
    connect = sqlite3.connect(DATABASE)
    c = connect.cursor()
    c.execute('SELECT LocationID,FACILITYNAME FROM AIRPORT')
    identities = c.fetchall()
    airports  =[]
    n = len(identities)
    for i in range(n):
        airports.append(identities[i][0])
        airports.append(identities[i][1]+' ('+identities[i][0]+')')
    c.close()
    connect.close()
    return airports

def current_year():
    return datetime.now(tz=pytz.timezone('US/Eastern')).year

class SearchForm(Form):
    autocomp1 = TextField('Insert Aiport #1',id = 'airport1_autocomplete')
    autocomp2 = TextField('Insert Aiport #2',id = 'airport2_autocomplete')

@app.route('/_autocomplete',methods=['GET'])
def autocomplete():
    search1 = request.args.get('airport1_autocomplete')
    app.logger.debug(search1)
    search2 = request.args.get('airport2_autocomplete')
    app.logger.debug(search2)
    return jsonify(json_list = get_airports())

@app.route("/")
@app.route("/home")
def home():
    year = current_year()
    form= SearchForm(request.form)
    mymap = Map(zoom=3,style="height:500px;width:800px;margin-left:auto;margin-right:auto;display:block;",
                identifier="view-side",
                lat=39.8283,
                lng=-98.5795,
                center_on_user_location = True,
                markers=[(39.8283,-98.5795)] #center of US,
            )
    return render_template('home.html',title = 'The Beginning',
    form=form,mymap=mymap,year = year)

@app.route("/",methods=['POST'])
def task():
    year = current_year()
    form  = SearchForm(request.form)
    text1 = form.autocomp1.data
    text2 = form.autocomp2.data
    mymap = Map(zoom=3,style="height:500px;width:800px;margin-left:auto;margin-right:auto;display:block;",
                identifier="view-side",
                lat=39.8283,
                lng=-98.5795,
                center_on_user_location = True,
                markers=[(39.8283,-98.5795)] #center of US,
            )
    if text1 and text2:
        if len(text1)>4:
            text1=text1.split(' ')[-1].replace('(','').replace(')','')
        if len(text2)>4:
            text2=text2.split(' ')[-1].replace('(','').replace(')','')
        connect = sqlite3.connect(DATABASE)
        c = connect.cursor()
        c.execute('SELECT LocationID,FacilityName,LATITUDE,LONGITUDE,CITY,STATE FROM AIRPORT WHERE LocationID = ?;',(text1.upper(),))
        x = c.fetchone()
        c.execute('SELECT LocationID,FacilityName,LATITUDE,LONGITUDE,CITY,STATE FROM AIRPORT WHERE LocationID = ?;',(text2.upper(),))
        y = c.fetchone()
        c.close()
        connect.close()
        if x and y:
            result = '{} ({}) of {}, {} and {} ({}) of {}, {} are {} NM away!'.format(x[1],x[0],x[4],x[5],y[1],y[0],y[4],y[5],nauticalCalc(x[2],x[3],y[2],y[3]))
            lat1 = x[2]/3600
            lng1 = x[3]/3600
            lat2 = y[2]/3600
            lng2 = y[3]/3600
            loc1 = x[0]
            loc2 = y[0]
            mymap = Map(
                zoom = 3,
                style="height:500px;width:800px;margin-left:auto;margin-right:auto;display:block;",
                identifier="view-side",
                lat=lat1,
                lng=lng1,
                center_on_user_location = True,
                fit_markers_to_bounds = True,
                markers=[
                  {
                     'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                     'lat': lat1,
                     'lng': lng1,
                     'infobox': "<b>"+loc1+"</b>"
                  },
                  {
                     'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                     'lat': lat2,
                     'lng': lng2,
                     'infobox': "<b>"+loc2+"</b>"
                  }
                ],
            )
        else:
            result ='The names are either not an Airport ID or a Facility Name. Please Try again.'
    else:
        # result = 'Please fill in the input spaces.'
        return Response(status=204)
    return render_template('home.html', result=result,
    form=form,mymap=mymap,year = year)

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__=='__main__':
    app.run(host='0.0.0.0',port=2004,debug=True)
