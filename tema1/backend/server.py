from flask import Flask, request, jsonify
from flask_cors import CORS
from reporting import createReport
from processData import * 

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ["POST"])
def sendForm():
    data = request.get_json()
    saveDataToDB(data)

    return "Done"

@app.route("/xml", methods = ["POST"])
def receiveXML():
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save("./" + filename)
    
    return "Done"

@app.route("/raport", methods = ["POST"])
def generateRaport():
    createReport()    

    return "Done"

if __name__ == "__main__":
    app.run()

