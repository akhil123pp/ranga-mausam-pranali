#!/usr/bin/env python
import flask
from scrape.collect import Fetch

app = flask.Flask("y-nakh naksa")
app.debug = True

fObj = Fetch()


@app.route("/")
def hello():
    return "Hello world!"


@app.route("/info/")
def infoPage():
    file = open("html/info.html", "r")
    lines = "".join(file.readlines())
    return lines


@app.route("/api/json/season/")
def getSeason():
    return flask.jsonify({"dataFound": 1, "season": fObj.getSeason()})


@app.route("/api/json/<string:location>")
def returnWeather(location):
    locData = fObj.getLocations()
    if location.lower() in locData:
        fObj.parsedData[location.lower()].update(
                {"dataFound": 1, "name": location})
        return flask.jsonify(fObj.parsedData[location.lower()])
    elif location.lower() == "all":
        fObj.parsedData.update({"dataFound": 1})
        return flask.jsonify(fObj.parsedData)
    return flask.jsonify({"dataFound": 0})


@app.route("/api/json/listLocations")
def listLocations():
    return flask.jsonify({"dataFound": 1, "locations": fObj.getLocations()})


@app.route("/api/json/bringUmbrella/<string:location>")
def bringUmbrella(location):
    data = fObj.parsedData.get(location.lower(), None)
    print data, "data"
    if data is not None:
        chanceOfRain = data.get("Chances of Rain", None)
        if chanceOfRain is not None:
            chanceOfRain = int(chanceOfRain.strip(" ").strip("%"))
            if chanceOfRain >= 40:
                bringUmbrella = 1
                dataFound = 1
            else:
                bringUmbrella = 0
                dataFound = 1
        else:
            dataFound = 0
    else:
        dataFound = 0
    if dataFound == 0:
        return flask.jsonify(
                {"dataFound": dataFound})
    else:
        return flask.jsonify(
                {'dataFound': dataFound, 'bringUmbrella': bringUmbrella})


if __name__ == "__main__":
    app.run()
