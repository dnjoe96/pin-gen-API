from app import app, db
from flask import jsonify
from app.models import Pin
import random


def random_digits(n):
    ''' A function to generate random 15 digit number. where n is the number of Digits'''
    lower = 10**(n-1)
    upper = 10**n - 1
    return random.randint(lower, upper)


@app.route('/generate', methods=['GET', 'POST'])
def index():
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

    return "s/n = {}, pin = {}".format(s_n1, pin1)


@app.route('/pin/<string:pin>', methods=['GET'])
def check_s_n(pin):
    pin = Pin.query.filter_by(pin=pin).all()
    if pin:
        return 'Valid Pin'


@app.route('/serial_no/<string:s_n>', methods=['GET'])
def check_pin(s_n):
    s_n = Pin.guery.filter_by(s_n=s_n).all()
    if s_n:
        return 'Valid Serial No'
