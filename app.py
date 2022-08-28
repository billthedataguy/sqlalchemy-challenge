# Import dependencies

import datetime as dt
from dateutil.relativedelta import relativedelta                

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify, escape

# Create dbase engine
 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect the dbase

Base = automap_base()

Base.prepare(engine, reflect=True)

# Make dbase objects

Measurement = Base.classes.measurement
Station = Base.classes.station

# Date conversion functions

def convert_from_iso(obj):    
    return dt.date.fromisoformat(obj)
        
def convert_to_iso(obj):    
    return dt.date.isoformat(obj)             

# Get constants populated for global access in flask app

session = Session(engine)

DATES = session.query(Measurement.date)
MAX_DATE = convert_from_iso(max(DATES)[0])
MIN_DATE = convert_from_iso(min(DATES)[0])
LAST_12_MONTHS = MAX_DATE - relativedelta(months=12)

STATIONS = session.query(Station.station).distinct().all()
STATION_LIST = [STATION[0] for STATION in STATIONS]

active_list = []
for STATION in STATION_LIST:
        row_counts = session.query(Measurement.station).filter(Measurement.station == STATION).count()
        active_list.append((row_counts, STATION))
    
MOST_ACTIVE_STATION = sorted(active_list, reverse=True)[0][1]

session.close()



#############################################################
# BEGIN FLASK ROUTING
#############################################################


app = Flask(__name__)


# Index endpoint

@app.route("/")
def index():

    # Using Flask escape function to deal with left and right angle brackets

    start_endpoint = escape("/api/v1.0/<startdate>")
    start_end_endpoint = escape("/api/v1.0/<startdate>/<enddate>")

    print("Server received request for 'Index' page...")
    return(
        f"<h1>Welcome to the Hawaii Weather API!</h1>"
        f"<h2><u>Available Routes:</u></h2>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"{start_endpoint} <b>e.g. /2022-08-28</b><br/><br/>"
        f"{start_end_endpoint} <b>e.g. /2022-08-07/2022-08-28</b><br/><br/>"       
        
          )

# Precipitation endpoint

@app.route("/api/v1.0/precipitation")
def precipitation():

    precip_dict = {}   
    
    session = Session(engine)

    LAST_12_MONTHS_str = convert_to_iso(LAST_12_MONTHS)
    
    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= LAST_12_MONTHS_str).all()
    precip_dict = dict(precip)
       
    session.close()  
  
    return jsonify(precip_dict)

# Stations endpoint

@app.route("/api/v1.0/stations")
def stations():
    
    return jsonify(STATION_LIST)

# Tobs endpoint

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)
    sel = [Measurement.date, Measurement.station, Measurement.tobs]

    LAST_12_MONTHS_str = convert_to_iso(LAST_12_MONTHS)

    tobs = session.query(*sel).filter(Measurement.station == MOST_ACTIVE_STATION).filter(Measurement.date >= LAST_12_MONTHS_str).all()
    
    # Serializer function

    def serialize(obj):
        return {
            "Date": obj[0],
            "Station": obj[1],
            "Tobs": obj[2]
               }
        
    session.close()

    the_tobs_data=[serialize(t) for t in tobs]

    return jsonify(the_tobs_data)

# <startdate> endpoint

@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    
    # Check if user has given a valid date

    try:

        start_date_str1 = convert_to_iso(convert_from_iso(start))
        
    except: 

        return f"START DATE PARSING PROBLEM"

    sel = [Measurement.date, Measurement.tobs,
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs)
       ]

    tobs_start = session.query(*sel).filter(Measurement.station == MOST_ACTIVE_STATION).filter(Measurement.date >= start_date_str1).all()
    
    MAX_DATE_str = convert_to_iso(MAX_DATE)

    # Serializer function 

    def serialize1(obj):
        return {
            "Date Range": f"Start = {start_date_str1} End = {MAX_DATE_str} (INCLUSIVE)",
            "Min": obj[2],
            "Avg": obj[3],
            "Max": obj[4]
               }
        
    session.close()

    the_tobs_start_data=[serialize1(t) for t in tobs_start]

    return jsonify(the_tobs_start_data)

# <startdate>/<enddate> endpoint

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    
    # Check if user has given a valid start and end date

    try:

        start_date_str2 = convert_to_iso(convert_from_iso(start))
        
        end_date_str2 = convert_to_iso(convert_from_iso(end))
        
    except: 

        return f"DATE PARSING PROBLEM"

    sel = [Measurement.date, Measurement.tobs,
       func.min(Measurement.tobs),
       func.avg(Measurement.tobs),
       func.max(Measurement.tobs)
       ]

    tobs_start_end = session.query(*sel).filter(Measurement.station == MOST_ACTIVE_STATION).filter(Measurement.date >= start_date_str2)\
                .filter(Measurement.date <= end_date_str2).all()
    
    # Serializer function

    def serialize2(obj):
        return {
            "Date Range": f"Start = {start_date_str2} End = {end_date_str2} (INCLUSIVE)",
            "Min": obj[2],
            "Avg": obj[3],
            "Max": obj[4]
               }
        
    session.close()

    the_tobs_start_end_data=[serialize2(t) for t in tobs_start_end]

    return jsonify(the_tobs_start_end_data)
    
if __name__ == "__main__":
    app.run(debug=True)

#############################################################
# END FLASK ROUTING
#############################################################