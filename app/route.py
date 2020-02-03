from app import app, db, mongo
from flask import jsonify
from app.models import Register, random_digits, twelve_digit_serial_no, database_serial_no


@app.route('/', methods=['GET'])
def index():
    """
    This is the end point for a resource that generates random 15digit pin and serial number when the
    resource is requested.

    it generates 15digits random pin, and verifies that pin does not already exists in the database
    before returning it to the client in JSON format.

    random_digit function is created with random function.
    :return: pin, serial
    """
    mongo_data = mongo.db.pin_data

    # implemnting while loop to ensure that the random generated pin doesn't already exist in the database
    counter = 1
    while counter >= 1:
        pin = random_digits(15)
        pin1 = mongo_data.find_one({'pin': pin})
        
        if pin1:
            print('again')
            counter = counter + 1
        else:
            print(pin)
            break

    save = Register(pin=str(pin))
    db.session.add(save)
    db.session.commit()
    serial_number = Register.query.filter_by(pin=str(pin)).first()
    pin1 = pin

    # storing to mongo db
    mongo_data.insert({'serial_no': serial_number.s_n, 'pin': pin1})
    return jsonify({'serial number': twelve_digit_serial_no(serial_number.s_n), 'PIN': pin1})


@app.route('/<string:serial_no>', methods=['GET'])
def check_pin(serial_no):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    s_n = database_serial_no(serial_no)

    # searching to mongo db
    mongo_data = mongo.db.pin_data
    search = mongo_data.find_one({'serial_no': s_n})

    if search:
        return jsonify({'message': 'Valid Serial No', 'pin': search['pin']})
    return jsonify({'message': 'Invalid serial No !!!'})
