from app import app, db, mongo, ussd
from flask import jsonify, request
from app.models import Register, random_digits, twelve_digit_serial_no
import requests


API_KEY = 'healthradar-95302420205yeeyqz'


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
    text = request.values.get("text","default")

    def_symptoms = ["tiredness", "dry_cough", "aches", "sore throat", "nasal_congestion", "runny nose", "muscle pain",
                    "difficulty in breathing", "swelling", "abdominal pain", "chest pain", "cardiac disorder",
                    "enlarged oesophagus", "neurological alterations", "diarrhoea", "blood in the stool",
                    "liver enlargement", "meningitis", "constipation"]

    symptoms = []
    data = []

    def func():
        global phone
        # print(data)
        save = data[-1]
        selection = []
        phone = save[0]

        for one in save:
            if len(one) != 11 and one != '0' and one != '00':
                selection.append(one)

        if len(selection) == 1:
            final_selection = list(selection[0])
        else:
            first_selection = list(selection[0])
            second_selection = selection[1]
            sel = []
            for i in selection[1]:
                sel.append(int(i) + 9)
            final_selection = first_selection + sel

        for i in final_selection:
            symptoms.append(def_symptoms[int(i) - 1])

        str1 = ""

        # converting list to string seperated with comma
        for y in symptoms:
            str1 += y + ','

        # here are the final symptoms according to the selection
        final_symptoms = str1[:-2]
        print(final_symptoms)

        # here is the phone number entered
        num = phone
        print(num)

        payload = {"patient_number": num, "provider_number": phone_number, "symptoms": final_symptoms}
        print(payload)
        requests.post("https://health-radar.herokuapp.com/api/patients", data=payload)

    # the phone number to pass into the Response

    if text == "":
        response = "CON Welcome to HealthRadar\n"
        # response += "Enter patient phone number to begin\n"
        response += "Enter your PIN to begin\n"

    # adding the layer to verify PIN
    elif len(text) == 5:
        request_headers = {"Authorization": "{}".format(API_KEY)}
        payload = {"phone": phone_number, "PIN": text}

        resp = requests.post('https://healthradarapp.herokuapp.com/api/v1/user/verify', data=payload,
                          headers=request_headers)

        if resp.status_code is 200:
            response = "END Thank you for using HealthRadar\n"
            response += "You have entered an invalid number."

    elif text.split('*')[1] == 11:
        # phone.append(text)
        save = text.split('*')
        data.append(save)
        print(save)
        response = "CON select symptoms\n"
        response += "1. Tiredness\n"
        response += "2. Dry cough\n"
        response += "3. Aches\n"
        response += "4. Soar throat\n"
        response += "5. Nasal Congestion\n"
        response += "6. Runny Nose\n"
        response += "7. Muscle pain\n"
        response += "8. Difficulty in breathing\n"
        response += "9. Swelling\n"
        response += "0. Next menu\n"
        response += "00. End session"

    elif text.split('*')[-1] != '0' and text.split('*')[-1] != '00':
        save = text.split('*')
        data.append(save)
        print(save)
        response = "CON select symptoms\n"
        response += "1. Tiredness\n"
        response += "2. Dry cough\n"
        response += "3. Aches\n"
        response += "4. Soar throat\n"
        response += "5. Nasal Congestion\n"
        response += "6. Runny Nose\n"
        response += "7. Muscle pain\n"
        response += "8. Difficulty in breathing\n"
        response += "9. Swelling\n"
        response += "0. Next menu\n"
        response += "00. End session"

    elif text.split('*')[-1] == '0':
        save = text.split('*')
        data.append(save)
        print(save)

        response = "CON select symptoms\n"
        response += "1. Abdominal Pain\n"
        response += "2. Chest pain\n"
        response += "3. Cardiac disorder\n"
        response += "4. Enlarged Oesophagus\n"
        response += "5. Neurological alterations\n"
        response += "6. diarrhoea\n"
        response += "7. Blood in the stool\n"
        response += "8. Liver enlargement\n"
        response += "9. Meningitis\n"
        response += "00. End session"

    elif text.split('*')[-1] == '00':
        save = text.split('*')
        data.append(save)
        print(save)
        func()
        response = "END Thank you for using HealthRader\n"
        response += "Data for {} has been captured \n".format(phone)
        response += "Data for has been captured \n"
        response += "Remember to call NCDC on \n"
        response += "080000101010 if you suspect COVID-19."

    return response


