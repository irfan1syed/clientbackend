
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

# MongoDB connection string (adjust as needed)
client = MongoClient("mongodb://localhost:27017/")
db = client['event_db']
collection = db['registrations']

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not all(k in data for k in ("name", "phone", "email", "location")):
        return jsonify({"message": "Invalid data"}), 400

    collection.insert_one(data)
    return jsonify({"message": f"Registered successfully for {data['name']}"}), 200

@app.route('/registrations', methods=['GET'])
def get_registrations():
    records = list(collection.find({}, {"_id": 0}))
    records.reverse()  # Show newest on top
    return jsonify(records)

if __name__ == '__main__':
    app.run(debug=True)

