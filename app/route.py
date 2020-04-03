from app import app, db, mongo, ussd
from flask import jsonify, request
from app.models import Register, random_digits, twelve_digit_serial_no


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
    sn = twelve_digit_serial_no(serial_number.s_n)

    # storing to mongo db
    mongo_data.insert({'serial_no': sn, 'pin': pin1, 'activation_status': 0})

    return jsonify({'serial number': sn, 'PIN': pin1})


@app.route('/check/<string:serial_no>', methods=['GET'])
def check_pin(serial_no):
    """
    This endpoint verifies that the pin entered matches with what is in the database.
    if it exists, return 'valid' else, returns 'Invalid
    """
    # searching to mongo db
    mongo_data = mongo.db.pin_data
    search = mongo_data.find_one({'serial_no': int(serial_no)})

    if search:
        return jsonify({'message': 'Valid Serial No', 'pin': search['pin']})
    return jsonify({'message': 'Invalid serial No !!!'})


# @app.route('/ussd', methods=['GET', 'POST'])
# def ussd():
#     global response
#     session_id = request.values.get("sessionId",None)
#     service_code = request.values.get("serviceCode",None)
#     phone_number = request.values.get("phoneNumber",None)
#     print(phone_number)
#     text = request.values.get("text","default")
#     sms_phone_number = []
#     sms_phone_number.append(phone_number)
#
#     if text == "":
#         response = "CON What would you like to do?\n"
#         response += "1. Check account details\n"
#         response += "2. Check phone number"
#
#     elif text == "1":
#         response = "CON What would you like to check on your account?\n"
#         response += "1. Account number\n"
#         response += "2. Account balance"
#
#     elif text == "2":
#         response = "END Your phone number is {}".format(phone_number)
#
#     elif text == "1*1":
#         account_number = "1243324376742"
#         response = "END Your account number is {}".format(account_number)
#
#     elif text == "1*2":
#         account_balance = "100,000"
#         response = "END Your account balance is KES {}".format(account_balance)
#
#     else:
#         response = "END Invalid input. Try again."
#
#     return response


@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    global response
    session_id = request.values.get("sessionId",None)
    service_code = request.values.get("serviceCode",None)
    phone_number = request.values.get("phoneNumber",None)
    print(phone_number)
    text = request.values.get("text","default")
    sms_phone_number = []
    sms_phone_number.append(phone_number)

    if text == "":
        response = "CON Welcome\n"
        response += "enter phone number\n"

    # elif len(text.split('*')[-1]) >= 11 or text.split('*')[-1] == '1':
    elif len(text) == 11:
        print(text)
        response = "CON select symptoms\n"
        response += "1. cough\n"
        response += "2. sneezing\n"
        response += "3. laughing\n"
        response += "4. shortness of breath\n"
        response += "5. body pain\n"
        response += "6. weakness\n"
        response += "0. next menu"

    elif text.split('*')[-1] != '0':
        save = text.split('*')
        print(save)
        response = "CON select symptoms\n"
        response += "1. cough\n"
        response += "2. sneezing\n"
        response += "3. laughing\n"
        response += "4. shortness of breath\n"
        response += "5. body pain\n"
        response += "6. weakness\n"
        response += "0. next menu\n"
        response += "00. End session"

    elif text.split('*')[-1] == '0':
        response = "CON select symptoms\n"
        response += "7. cough\n"
        response += "8. sneezing\n"
        response += "9. laughing\n"
        response += "10. shortness of breath\n"
        response += "11. body pain\n"
        response += "12. weakness\n"
        response += "00. End session"

    elif text.split('*')[-1] != '00':
        save = text.split('*')
        print(save)
        response = "CON select symptoms\n"
        response += "7. cough\n"
        response += "8. sneezing\n"
        response += "9. laughing\n"
        response += "10. shortness of breath\n"
        response += "11. body pain\n"
        response += "12. weakness\n"
        response += "00. End session"

    elif text.split('*')[-1] == '00':
        response = "END data captured."



    # elif text == "2":
    #     response = "END Your phone number is {}".format(phone_number)
    #
    # elif text == "1*1":
    #     account_number = "1243324376742"
    #     response = "END Your account number is {}".format(account_number)
    #
    # elif text == "1*2":
    #     account_balance = "100,000"
    #     response = "END Your account balance is KES {}".format(account_balance)
    #
    # else:
    #     response = "END Invalid input. Try again."

    return response