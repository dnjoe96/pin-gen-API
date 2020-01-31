from app import app, db
from flask import jsonify
from app.models import Pin
import random


def random_digits(n):
    """ A function to generate random 15 digit number. where n is the number of Digits"""
    lower = 10**(n-1)
    upper = 10**n - 1
    return random.randint(lower, upper)


@app.route('/', methods=['GET'])
@app.route('/pin', methods=['GET'])
def index():
    """
    This is the end point for a resource that generates random 15digit pin and serial number when the
    resource is requested.

    it generates 15digits random pin, and verifies that pin does not already exists in the database
    before returning it to the client in JSON format.

    random_digit function is created with random function.
    :return: pin, serial
    """
    # generating random pin and s_n
    pin1 = random_digits(15)
    print(pin1)
    s_n1 = random.randrange(1000,9999)
    print(s_n1)
    pin_db = Pin.query.filter_by(pin=str(pin1)).all()
    s_n_db = Pin.query.filter_by(s_n=int(s_n1)).all()

    # implementing a recursive function
    if pin_db or s_n_db:
        pin1 = random_digits(15)
        s_n1 = random.randrange(10, 100)

    save = Pin(s_n=int(s_n1), pin=str(pin1))
    db.session.add(save)
    db.session.commit()
    serial_number = s_n1
    pin = pin1
    return jsonify({'serial number': serial_number, 'PIN': pin})


@app.route('/pin/<string:pin>', methods=['GET'])
def check_s_n(pin):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    pin = Pin.query.filter_by(pin=pin).all()
    if pin:
        return jsonify({'message': 'Valid PIN'})
    return jsonify({'message': 'Invalid PIN !!!'})


@app.route('/serial_no/<string:s_n>', methods=['GET'])
def check_pin(s_n):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    s_n = Pin.guery.filter_by(s_n=s_n).all()
    if s_n:
        return jsonify({'message': 'Valid Serial No'})
    return jsonify({'message': 'Invalid serial No !!!'})