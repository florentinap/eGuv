from flask import Flask, request, jsonify
from flask_cors import CORS
from frontendAux import *

app = Flask(__name__)
CORS(app)

@app.route("/allMinister")
def allMinister():
    result = getAllMinisters()

    return jsonify(result)

@app.route("/pap", methods = ["POST"])
def pap():
    minister = request.json['minister']
    result = getPap(JSON.stringify(minister))

    return jsonify(result)

@app.route("/data")
def data():
    result = getData()
    return jsonify(result)



if __name__ == "__main__":
    app.run()
