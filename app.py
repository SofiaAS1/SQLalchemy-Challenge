from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Welcome to my 'Home' page!"

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'precipitation' page...")
    return "Welcome to my 'Precipitation' page!"

@app.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' page...")
    return "Welcome to my 'stations' page!"

@app.route("/api/v1.0/tobs")
def TObs():
    print("Server received request for 'TObs' page...")
    return "Welcome to my 'TObs' page!"

@app.route("/api/v1.0/<start>")
def Start():
    print("Server received request for 'Start' page...")
    return "Welcome to my 'Start' page!"

@app.route("/api/v1.0/<start>/<end>")
def SnE():
    print("Server received request for 'SnE' page...")
    return "Welcome to my 'Start & End' page!"

if __name__ == "__main__":
    app.run(debug=True)