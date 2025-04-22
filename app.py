from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Replace with your actual connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nomorepasses&49@db.fesxheyctetkwusyhlgs.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define registration model
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    location = db.Column(db.String(120))

# Create tables
with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    new_entry = Registration(
        name=data['name'],
        phone=data['phone'],
        email=data['email'],
        location=data['location']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Registration successful!'})

@app.route('/registrations', methods=['GET'])
def get_all():
    all_regs = Registration.query.order_by(Registration.id.desc()).all()
    result = [
        {
            'name': r.name,
            'phone': r.phone,
            'email': r.email,
            'location': r.location
        }
        for r in all_regs
    ]
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
