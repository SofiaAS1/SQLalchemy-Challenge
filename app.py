from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    return (
        f"Welcome to The Climate App API!<br/>"
        f"<br/>"
        f"Available Routes are:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"<br/>"
        f"May Your Days Be Bright & Sunny!"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    return "Welcome to my 'Precipitation' page!"

@app.route("/api/v1.0/stations")
def stations():
    return "Welcome to my 'stations' page!"

@app.route("/api/v1.0/tobs")
def TObs():
    return "Welcome to my 'TObs' page!"

@app.route("/api/v1.0/<start>")
def Start():
    return "Welcome to my 'Start' page!"

@app.route("/api/v1.0/<start>/<end>")
def SnE():
    return "Welcome to my 'Start & End' page!"

if __name__ == "__main__":
    app.run(debug=True)