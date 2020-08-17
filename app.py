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
        f"/api/v1.0/start (start date must be in quotes & in mm-dd format) <br/>"
        f"/api/v1.0/start/end (start & end dates must be in quotes & in yyyy-mm-dd format) <br/>"
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
def start(start):
    tmin = func.min(measurement.tobs)
    tavg = func.avg(measurement.tobs)
    tmax = func.max(measurement.tobs)
    sel = [tmin, tavg, tmax]
    result = session.query(*sel).filter(func.strftime("%m-%d", measurement.date) >= start).all()
    start = []
    for tmin, tavg, tmax in result:
        start_dict = {}
        start_dict["tmin"] = tmin
        start_dict["tavg"] = tavg
        start_dict["tmax"] = tmax
        start.append(start_dict)

    return jsonify(start)

@app.route("/api/v1.0/<start>/<end>")
def SnE(start, end):
    tmin = func.min(measurement.tobs)
    tavg = func.avg(measurement.tobs)
    tmax = func.max(measurement.tobs)
    sel = [tmin, tavg, tmax]
    result = session.query(*sel).filter(measurement.date >= start).filter(measurement.date <= end).all()
    end = []
    for tmin, tavg, tmax in result:
        end_dict = {}
        end_dict["tmin"] = tmin
        end_dict["tavg"] = tavg
        end_dict["tmax"] = tmax
        end.append(end_dict)

    return jsonify(end)

if __name__ == "__main__":
    app.run(debug=True)