from app import app, db
from flask import jsonify
from app.models import Register
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
    pin = random_digits(15)
    s_n = random.randrange(1000,9999)
    pin1 = Register.query.filter_by(pin=str(pin)).all()
    s_n1 = Register.query.filter_by(s_n=int(s_n)).all()

    # implementing a recursive function
    if pin1 or s_n1:
        pin = random_digits(15)
        s_n = random.randrange(1000, 9999)

    # save = Register(s_n=int(s_n), pin=str(pin))
    # db.session.add(save)
    # db.session.commit()
    serial_number = s_n
    pin1 = pin
    return jsonify({'serial number': serial_number, 'PIN': pin1})

@app.route('/<string:pin>', methods=['GET'])
@app.route('/pin/<string:pin>', methods=['GET'])
def check_s_n(pin):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    pin = Register.query.filter_by(pin=pin).all()
    if pin:
        return jsonify({'message': 'Valid PIN'})
    return jsonify({'message': 'Invalid PIN !!!'})


@app.route('/serial_no/<string:s_n>', methods=['GET'])
def check_pin(s_n):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    s_n = Register.query.filter_by(s_n=s_n).all()
    if s_n:
        return jsonify({'message': 'Valid Serial No'})
    return jsonify({'message': 'Invalid serial No !!!'})