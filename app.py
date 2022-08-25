import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################




app = Flask(__name__)


@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return(
        f"Welcome to the Hawaii Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
          )




@app.route("/api/v1.0/precipitation")
def precipitation():
       
    session = Session(engine)

    results = session.query(Passenger.name).all()

    session.close()

    all_names = list(np.ravel(results))

    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def stations():
        
    session = Session(engine)
   
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_passengers = []

    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
   
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_passengers = []

    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)

@app.route("/api/v1.0/<start>")
def start():
    session = Session(engine)
   
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_passengers = []

    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)

@app.route("/api/v1.0/<start>/<end>")
def start_end():
    session = Session(engine)
   
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()

    session.close()

    all_passengers = []

    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)

    
if __name__ == "__main__":
    app.run(debug=True)

