from flask import Flask, render_template, request, redirect, url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rainbow_table.db'
app.config['SECRET_KEY'] = 'ASDFGFEJNNEJDNJKEWNIWF'

db = SQLAlchemy(app)

class Ambulance(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    number_plate = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(64), nullable=True)
    active = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f"Ambulance(id={self.id}, password_hash='{self.password_hash}', plaintext_password='{self.plaintext_password}')"

with app.app_context():
    db.create_all()

import hashlib
from flask import request, jsonify

@app.route('/update', methods=['GET', 'POST'])
def index():
    num_pl = request.args.get('num_pl')
    location = request.args.get('location')
    active = request.args.get('active')
    result = Ambulance.query.filter_by(number_plate=num_pl).first()
    if result:
        if active=="False":
            db.session.delete(result)
            response = {"message": "removed"}
        else:
            
            result.location=location
            result.active='True'
            response = {"message": "updated"}
        db.session.commit()
        return response
    else:
        try:
            n_e = Ambulance(number_plate=num_pl,location=location,active=active)
            db.session.add(n_e)
            db.session.commit()
            response = {"message": "record_added"}
            return response
        except Exception as e:
            return {'message':f'Failed {e}'}


@app.route('/ambulances', methods=['GET'])
def get_ambulances():
    ambulances = Ambulance.query.all()
    ambulance_list = []
    for ambulance in ambulances:
        ambulance_data = {
            'id': ambulance.id,
            'number_plate': ambulance.number_plate,
            'location': ambulance.location,
            'active': ambulance.active
        }
        ambulance_list.append(ambulance_data)
    return jsonify({'ambulances': ambulance_list})


@app.route('/view_table')
def view_table():
    entries = Ambulance.query.all()
    return render_template('view_table.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)