import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

session = Session(engine)

@app.route("/")
def home():

    return (
        f"Welcome to Sofie's OFFICIAL Climate App API!<br/>"
        f"<br/>"
        f"Available Routes are:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"<br/>"
        f"May Your Days Be Bright & Sunny, but Your Hair NEVER Frizzy!"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    lastDate = session.query(func.max(measurement.date)).all()[0][0]
    lastDate = dt.datetime.strptime(lastDate, '%Y-%m-%d')
    priorYear = lastDate - dt.timedelta(365)
    result = session.query(measurement.date, measurement.prcp).filter(measurement.date>=priorYear).all()
    precipitation = []
    for date, prcp in result:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(station.station,station.name)\
    .group_by(station.name)\
    .order_by(station.name)\
    .all()

    stations = list(np.ravel(results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def TObs():
    lastDate = session.query(func.max(measurement.date)).all()[0][0]
    lastDate = dt.datetime.strptime(lastDate, '%Y-%m-%d')
    priorYear = lastDate - dt.timedelta(365)
    results = session.query(measurement.tobs, measurement.date)\
    .filter(measurement.station == 'USC00519281', measurement.date>=priorYear).all()

    TObs = list(np.ravel(results))

    return jsonify(TObs)

@app.route("/api/v1.0/<start>")
def start():
    date = "%m-%d"
    min = func.min(measurement.tobs)
    avg = func.avg(measurement.tobs)
    max = func.max(measurement.tobs)
    sel = [min, avg, max]
    result = session.query(*sel).filter(func.strftime("%m-%d", measurement.date) >= date).all()
    start = []
    for min, avg, max in result:
        start_dict = {}
        start_dict["min"] = TMin
        start_dict["avg"] = TAvg
        start_dict["max"] = TMax
        start.append(start_dict)

    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def SnE():
    return "Welcome to my 'Start & End' page!"

if __name__ == "__main__":
    app.run(debug=True)