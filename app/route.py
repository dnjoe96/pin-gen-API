from app import app, db
from flask import jsonify
from app.models import Register, random_digits, twelve_digit_serial_no, database_serial_no


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
    # implemnting while loop to ensure that the random generated pin doesn't already exist in the database
    counter = 1
    while counter >= 1:
        pin = random_digits(15)
        pin1 = Register.query.filter_by(pin=str(pin)).all()
        
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
    return jsonify({'serial number': twelve_digit_serial_no(serial_number.s_n), 'PIN': pin1})


@app.route('/check/<string:serial_no>', methods=['GET'])
def check_pin(serial_no):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    s_n = database_serial_no(serial_no)
    search = Register.query.filter_by(s_n=s_n).first()
    if search:
        return jsonify({'message': 'Valid Serial No', 'pin': search.pin})
    return jsonify({'message': 'Invalid serial No !!!'})
