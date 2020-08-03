import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#Home page
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start (Please enter a start date format YYYY-MM-DD instead of start)<br/>"
        f"/api/v1.0/start/end (Please enter start/end dates format YYYY-MM-DD/YYYY-MM-DD instead of start/end)"
    )

#Precipitation page
@app.route("/api/v1.0/precipitation")

def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   
    """Return a list of precipitation over the last 12 months"""
    # Query the precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_ago).all()
    
    session.close()

    # Create a dictionary from the row data
    all_results = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_results.append(prcp_dict)

    return jsonify(all_results)

#Stations page
@app.route("/api/v1.0/stations")

def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    """Return a list of all stations"""
    # Query all stations
    stations = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)

#TOBS page
@app.route("/api/v1.0/tobs")

def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)   
    """Return a list of temperatures over the last 12 months"""
    # Query the temperature data for the last 12 months for the most active station
    temperatures = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date > year_ago).\
    filter(Measurement.station == 'USC00519281').all()

    session.close()

   # Convert list of tuples into normal list
    temp_list = list(np.ravel(temperatures))

    return jsonify(temp_list)

#Start date page
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Convert a string date into a datetime object
    date_time_obj = dt.datetime.strptime(start, '%Y-%m-%d')
    search_date = date_time_obj.date()
    
    # Query the min, max and average temperature data for dates above the start date
    min_max_avg_temp = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= search_date).all()

    session.close()

   # Convert list of tuples into normal list
    temp_list2 = list(np.ravel(min_max_avg_temp))

    return jsonify(temp_list2)

#Start/End date page
@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Convert a string date into a datetime object
    start_date_time_obj = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date_time_obj = dt.datetime.strptime(end, '%Y-%m-%d')
    start_date = start_date_time_obj.date()
    end_date = end_date_time_obj.date()

    # Query the min, max and average temperature data for dates above the start date
    min_max_avg_temp2 = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start_date).\
    filter(Measurement.date <= end_date).all()

    session.close()

   # Convert list of tuples into normal list
    temp_list3 = list(np.ravel(min_max_avg_temp2))

    return jsonify(temp_list3)

if __name__ == '__main__':
    app.run(debug=True)




