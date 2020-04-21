from flask import Flask, request, make_response
import requests, json
from flask_pymongo import PyMongo
from datetime import datetime, date
import africastalking
import os
from app import app

PAYSTACK_AUTHORIZATION_KEY = 'sk_test_5eeb6cdd6ab278395a83868075660798028f62f0'

# africastalking.initialize(username, api_key)

# sms = africastalking.SMS

mongo = PyMongo(app)
# redis = FlaskRedis()
pin_error = "END Invalid PIN"
error = "END Invalid Account details"
cancel = "END Thank you!"
transaction_error = "END Unable to process transaction"


def cur_time_and_date():
    now = datetime.utcnow()
    today = date.today()
    d2 = today.strftime("%B %d, %Y")
    tm = now.strftime("%H:%M:%S")
    return (d2 + ' ' + 'at' + ' ' + tm)


def ussd_proceed(response):
    return "CON {}".format(response)


def ussd_stop(response):
    return "END {}".format(response)


def ussd_dep_stop(menu):
    return "END {}".format(menu)


def get_pin():
    response = "Welcome to HealthRadar\n"
    response += "Please Enter PIN to login\n"
    return ussd_proceed(response)


def welcome():
    response = "Welcome to HealthRadar, the public health "
    response += "surveillance and early warning system.\n"
    response += "+health workers, dial *347*61*1#\n"
    response += "+dial *347*61*2# for COVID-19 self-test"
    return ussd_stop(response)


def depoit_menu():
    menu = "Welcome to Instant Deposit Ltd.\n"
    menu += "Dial *384*95704*PIN*ACC*CD#\n"
    menu += "To start depositing"
    return ussd_dep_stop(menu)


def display_menu():
    # main menu
    response = "Welcome to HealthRadar\n"
    response += "Please enter patient phone number to proceed\n"
    return ussd_proceed(response)


def first_menu():
    response = "Select symptoms (example: 147)\n"
    response += "1. Fever\n"
    response += "2. Dry cough\n"
    response += "3. Myalgia or Arthralgia\n"
    response += "4. Fatigue\n"
    response += "5. Sputum production\n"
    response += "6. Shortness of breath\n"
    response += "7. Sore throat\n"
    response += "8. Headache\n"
    response += "9. Chills\n"
    response += "0. More Symptoms\n"
    # response += "00. Submit"
    return ussd_proceed(response)


def second_menu():
    response = "Select symptoms (example: 147)\n"
    response += "1. Fever\n"
    response += "2. Dry cough\n"
    response += "3. Myalgia or Arthralgia\n"
    response += "4. Fatigue\n"
    response += "5. Sputum production\n"
    response += "6. Shortness of breath\n"
    response += "7. Sore throat\n"
    response += "8. Headache\n"
    response += "9. Chills\n"
    response += "0. More Symptoms\n"
    response += "00. Submit"
    return ussd_proceed(response)


def third_menu():
    response = "Select symptoms (example: 147)\n"
    response += "1. Diarrhea\n"
    response += "2. Nasal congestion\n"
    response += "3. Nause or vomiting\n"
    response += "4. Hemoptysis\n"
    response += "5. Conjuntival\n"
    response += "6. Meningitis\n"
    response += "7. Constipation\n"
    response += "8. Chest pain\n"
    response += "9. Abdominal Pain\n"
    response += "00. None"
    return ussd_proceed(response)


def first_menu1():
    response = "Step 1 of 3\n"
    response += "Select symptoms (example: 147)\n"
    response += "1. Fever\n"
    response += "2. Dry cough\n"
    response += "3. Cold\n"
    response += "4. Fatigue\n"
    response += "5. Sputum production\n"
    response += "6. Shortness of breath\n"
    response += "7. Sore throat\n"
    response += "8. Headache\n"
    response += "9. Chills\n"
    response += "0. None"
    # response += "00. Continue"
    return ussd_proceed(response)

def hausa_menu():
    response = "Shashi na 1 cikin 3\n"
    response += "Zabi alamonin da kake ajikin kaa yanzu (misali: zabi numba data face daga 1 zuwa 0)\n"
    response += "1. Zazzabi\n"
    response += "2. Tari da bushwewar makogaro\n"
    response += "3. Mura\n"
    response += "4. Ciwon Jiki\n"
    response += "5. Daukewar numfashi\n"
    response += "6. Ciwon Kai\n"
    response += "7. Babu Ko wanne\n"
    response += "0. None"
    # response += "00. Continue"
    return ussd_proceed(response)


def third_menu1():
    response = "Step 1 of 3\n"
    response += "Select symptoms (example: 147)\n"
    response += "1. Diarrhea\n"
    response += "2. Nasal congestion\n"
    response += "3. Nause or vomiting\n"
    response += "4. Hemoptysis\n"
    response += "5. Conjuntival\n"
    response += "6. Meningitis\n"
    response += "7. Constipation\n"
    response += "8. Chest pain\n"
    response += "9. Abdominal Pain\n"
    response += "0. Continue"
    # response += "00. Submit"
    return ussd_proceed(response)


HealthRadar_API_KEY = 'healthradar-95302420205yeeyqz'

##########################################################################################


bk_cds = [
    {
        "name": "Access Bank",
        "code": "044"
    },
    {
        "name": "Citibank Nigeria",
        "code": "023"
    },
    {
        "name": "Diamond Bank",
        "code": "063"
    },
    {
        "name": "Ecobank Nigeria",
        "code": "050"
    },
    {
        "name": "Enterprise Bank",
        "code": "084"
    },
    {
        "name": "Fidelity Bank",
        "code": "070",
    },
    {
        "name": "First Bank of Nigeria",
        "code": "011"
    },
    {
        "name": "First City Monument Bank",
        "code": "214"
    },
    {
        "name": "Guaranty Trust Bank",
        "code": "058",
    },
    {
        "name": "Heritage Bank",
        "code": "030"
    },
    {
        "name": "Keystone Bank",
        "code": "082"
    },
    {
        "name": "MainStreet Bank",
        "code": "014"
    },
    {
        "name": "Skye Bank",
        "code": "076"
    },
    {
        "name": "Stanbic IBTC Bank",
        "code": "221"
    },
    {
        "name": "Standard Chartered Bank",
        "code": "068"
    },
    {
        "name": "Sterling Bank",
        "code": "232"
    },
    {
        "name": "Union Bank of Nigeria",
        "code": "032",

    },
    {
        "name": "United Bank For Africa",
        "code": "033"
    },
    {
        "name": "Unity Bank",
        "code": "215"
    },
    {
        "name": "Wema Bank",
        "code": "035"
    },
    {
        "name": "Zenith Bank",
        "code": "057"
    }
]


@app.route('/medic', methods=['GET', 'POST'])
def medic():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    # phone_number = '+2349018858924'
    text = request.values.get("text", "default")

    sms_phone_number = []

    sms_phone_number.append(phone_number)

    def_symptoms = ["fever", "dry_cough", "myalgia_or_arthralgia", "fatgue", "sputum_production",
                    "shortness_of_breath", "sore_throat", "headache", "chills", "diarrhea", "nasal_congestion",
                    "nausea_or_vomiting", "hemoptysis", "conjuntival", "meningitis", "constipation", "chest_pain",
                    "abdominal_pain"]

    def depo():
        session_id = request.values.get("sessionId", None)
        service_code = request.values.get("serviceCode", None)
        phoneNumber = request.values.get("phoneNumber", None)
        text = request.values.get("text", None)
        mongo_data = mongo.db.voucher
        ussd_details = mongo.db.details

        textArray = text.split("*") if text else text

        userResponse = textArray[-1] if isinstance(textArray, list) else text

        if userResponse == 0 or userResponse == '':
            # main menu
            menu = depoit_menu()

        elif len(text.split('*')[0]) == 15:
            try:

                pins = text.split('*')[0]
                account = text.split('*')[1]
                code = text.split('*')[2]
                find_pin = mongo_data.find_one({"pin": pins, "activation_status": 1})

                request_headers = {"Authorization": "Bearer {0}".format(PAYSTACK_AUTHORIZATION_KEY),
                                   "Content-Type": "application/json"}
                payload = {"account_number": account, "bank_code": code}
                print(payload)
                responses = requests.get('https://api.paystack.co/bank/resolve', params=payload,
                                         headers=request_headers)
                name = json.loads(responses.content)

                def status_code():
                    if responses.status_code in [200, 201]:
                        return 'verified'

                responses1 = status_code()

                if find_pin:
                    def get_pin_amount_by_batch():
                        bat = find_pin['batch']
                        batches = (list(map(int, ' '.join(str(bat)).split())))[0]
                        val = batches
                        if val == 1:
                            amts = '1,000'
                        elif val == 2:
                            amts = '2,000'
                        elif val == 3:
                            amts = '5,000'
                        elif val == 4:
                            amts = '10,000'
                        elif val == 5:
                            amts = '20,000'
                        else:
                            amts = ''
                        return amts

                    amt = get_pin_amount_by_batch()
                    if responses1:
                        acc_name = name['data']['account_name']
                        menu = "CON Enter 1 to Confirm deposit of NGN{} to {} \nA/C, {} \nEnter 0 to Cancel".format(
                            amt, acc_name, account)

                        if userResponse == "1":
                            try:
                                sms_response = sms.send("Your transaction is processing", sms_phone_number)
                                print(sms_response)
                                menu = 'END you will recieve an sms shortly'

                                # def get_phone():
                                #     for hello in sms_phone_number:
                                #         return hello
                                # phone = get_phone()
                                phone = '0' + phoneNumber[4:]

                                def get_bank_name():
                                    for codes in bk_cds:
                                        if codes['code'] == code:
                                            return codes['name']

                                bank = get_bank_name()
                                ussd_details.insert({"pin": pins, "account_number": account, "account_name": acc_name,
                                                     "amount": "NGN" + amt, "bank": bank, "phone": phone,
                                                     "transaction_date": cur_time_and_date()})
                            except Exception as e:
                                print("Mike, we have a problem : {}".format(e))
                        elif userResponse == "0":
                            menu = cancel
                    else:
                        menu = error
                else:
                    menu = pin_error

            except IndexError:
                menu = depoit_menu()
        else:
            menu = "END Invalid Input"

        resp = make_response(menu, 200)
        resp.headers["Content-type"] = "text/plain"
        return resp

    symptoms = []
    data = []
    travel = []
    contact = []

    def func(phones):
        global phone
        print('data', data)
        save = data[-1]
        print('save', save)
        selection = []
        phone = save[2]

        if len(save[2]) == 11:
            for one in save:
                if len(one) != 11 and one != '0' and one != '00':
                    selection.append(one)

            selections = selection[2:]
        else:
            selections = [save[1]]

        print(selection)
        print(selections)

        if len(selections) == 1:
            final_selection = list(selections[0])
        else:
            first_selection = list(selections[0])
            second_selection = selections[1]
            sel = []
            for i in second_selection:
                sel.append(int(i) + 9)
            final_selection = first_selection + sel

        # print(final_selection)
        if selections == '0':
            final_symptoms = 'None'
        else:
            symptoms = []
            for i in final_selection:
                symptoms.append(def_symptoms[int(i) - 1])

            str1 = ""

            # converting list to string seperated with comma
            for y in symptoms:
                str1 += y + ','

            # here are the final symptoms according to the selection
            final_symptoms = str1[:-1]

        print(final_symptoms)

        # here is the phone number entered
        patient_number = phone if len(save[2]) == 11 else phones
        provider_number = '0' + phone_number[4:] if len(save[2]) == 11 else phones

        contact_check = contact[0] if len(contact) > 0 else None
        travel_check = travel[0] if len(travel) > 0 else None



        payloads = {
            "patient_number": patient_number,
            "provider_number": provider_number,
            "symptoms": final_symptoms,
            "close_contact": contact_check,
            "traveled_out": travel_check
        }
        print(payloads)

        requests.post("https://health-radar.herokuapp.com/api/patients", data=payloads)

        # the phone number to pass into the Response

    try:

        if text == "":
            response = welcome()
        elif text == "1":
            response = get_pin()

        #################################### self test ###########################################
        elif text == "2":
            response = first_menu1()  # to self help

        elif len(text.split('*')) == 2 and text.split('*')[0] == '2':
            # elif text.split('*')[0] == '2' and ('00' not in text.split("*")):
            save = text.split('*')
            print(save)
            response = "CON Step 2 of 3\n"
            response += "Have you travelled out of Nigeria in the past 2 weeks?\n"
            response += "1. Yes\n2. No"

        # self test ending
        elif (text.split('*')[-1] == "1" or text.split('*')[-1] == "2") and len(text.split('*')) == 3 and \
                text.split('*')[0] == '2':
            save = text.split('*')
            print(save)

            response = "CON Step 3 of 3\n"
            response += "Do you know anyone having high fever, dry cough or difficulty in breathing?\n"
            response += "1. Yes\n2. No"

        # self test ending
        elif (text.split('*')[-1] == "1" or text.split('*')[-1] == "2") and len(text.split('*')) == 4 and \
                text.split('*')[0] == '2':
            save = text.split('*')
            data.append(save)
            print(save)
            if text.split('*')[-1] == "1":
                close_contact = 1
            else:
                close_contact = 2
            contact.append(close_contact)

            if text.split('*')[-2] == "1":
                traveled_out = 1
            else:
                traveled_out = 2
            travel.append(traveled_out)

            print(contact)
            print(travel)
            func(phone_number)
            phones = phone_number

            response = "END Thank you for taking this voluntary test for COVID-19. Remember:\n"
            response += "+ Always wash your hands with soap and running water\n"
            response += "+ No gathering"

        elif (text.split('*')[-1] != "1" or text.split('*')[-1] != '2' or text.split('*')[-1] != '0') and \
                text.split('*')[0] == '2':
            save = text.split('*')
            data.append(save)
            print(save)

            response = "END Thank you for taking this voluntary test for COVID-19. error"


        ###################################### End self test #########################################

        ############################## Hausa Test start ########################################

        elif text == "3":
            response = "CON Shashi na 1 cikin 3\n"
            response += "Zabi alamonin da kake ajikin kaa yanzu (misali: zabi numba data face daga 1 zuwa 0)\n"
            response += "1. Zazzabi\n"
            response += "2. Tari da bushwewar makogaro\n"
            response += "3. Mura\n"
            response += "4. Ciwon Jiki\n"
            response += "5. Daukewar numfashi\n"
            response += "6. Ciwon Kai\n"
            response += "7. Babu Ko wanne\n"
            response += "0. None"

        elif len(text.split('*')) == 2 and text.split('*')[0] == '3':
            # elif text.split('*')[0] == '2' and ('00' not in text.split("*")):
            save = text.split('*')
            print(save)
            response = "CON Shashi na 2 cikin 3\n"
            response += "Shin kayi tafiya zuwa kashashen waje a cikin sati biyu da suka wuce?\n"
            response += "1. E\n2. A'a"

        # self test ending
        elif (text.split('*')[-1] == "1" or text.split('*')[-1] == "2") and len(text.split('*')) == 3 and \
                text.split('*')[0] == '3':
            save = text.split('*')
            print(save)
            if text.split('*')[-1] == "1":
                traveled_out = 1
            else:
                traveled_out = 2
            travel.append(traveled_out)
            print(travel)
            response = "CON Shashi na 3 cikin 3\n"
            response += "Ko kasan wani da yake dauke da zazzabi ma zafi, ko tari, ko Kuma yake samun matsalar yin numfashi?\n"
            response += "1. E\n2. A'a"

        # self test ending
        elif (text.split('*')[-1] == "1" or text.split('*')[-1] == "2") and len(text.split('*')) == 4 and \
                text.split('*')[0] == '3':
            save = text.split('*')
            data.append(save)
            print(save)
            if text.split('*')[-1] == "1":
                close_contact = 1
            else:
                close_contact = 2
            contact.append(close_contact)

            print(contact)
            func(phone_number)
            phones = phone_number

            response = "END Mungode da tuntubarmu. Zamu nemeka idan akwai hukatar hakan.\n"
            response += "+ Tabbata Ka wanke hannuka da sabulu da kuma ruwa mai gudana\n"
            response += "+ Guji hallartar guraren dake da sama da mutane goma"

        elif (text.split('*')[-1] != "1" or text.split('*')[-1] != '2' or text.split('*')[-1] != '0') and \
                text.split('*')[0] == '3':
            save = text.split('*')
            data.append(save)
            print(save)

            response = "END Thank you for taking this voluntary test for COVID-19. error"

        ############################ Hausa Test End ######################################

        # example when a user pass *384*12745*321344688264392*2090209790*033#
        elif len(text.split("*")[0]) == 15:
            response = depo()

        ####################### HealthRadar for Providers ########################################
        elif len(text.split("*")[1]) == 4 and len(text.split("*")) == 2 and text.split('*')[0] != '2' and (
                '00' not in text.split("*")):

            pin = text.split("*")[1]

            phones = '0' + phone_number[4:]

            request_headers = {"Authorization": HealthRadar_API_KEY}
            payload = {"phone": phones, "PIN": pin}
            print(payload)
            r = requests.post('https://healthradarapp.herokuapp.com/api/v1/user/verify', data=payload,
                              headers=request_headers)

            print(json.loads(r.content)['success'])

            response = display_menu()
            print(text.split("*"))

            # if json.loads(r.content)['success'] == False:
            #     response = "END Thank you for using HealthRadar\n"
            #     response += "You are not yet registered.\n"
            #     response += "visit HealthRadar.ng for more info."
            # else:
            #     response = display_menu()
            #     print(text.split("*"))

        elif len(text.split("*")[2]) == 11 and len(text.split("*")) == 3 and text.split("*")[0] == '1' \
                and ('00' not in text.split("*")) and ('0' not in text.split("*")):
            save = text.split('*')[2]
            print(save)

            # this layer ensures that the phone number is correct, else error
            if len(text.split("*")[2]) == 11:
                response = first_menu()
            else:
                response = "END Thank you for using HealthRadar\n"
                response += "You have entered an invalid number."

        # elif text.split('*')[-1] != '0' and text.split('*')[0] != '2' and text.split('*')[-1] != '00' and (
        #         '00' not in text.split("*")) and ('0' not in text.split("*")):
        #     save = text.split('*')
        #     print(save)
        #
        #     this layer ensures that the phone number is correct, else error
            # if len(text.split("*")[2]) == 11:
            #     response = second_menu()
            # else:
            #     response = "END Thank you!\n"
            #     response += "You have entered an invalid Entry."

        elif len(text.split('*')) == 4 and text.split('*')[0] == '1' and ('00' not in text.split("*")):
            save = text.split('*')
            print(save)
            response = third_menu()

        elif len(text.split('*')) == 5 and text.split('*')[0] == '1':
            save = text.split('*')
            data.append(save)

            saves = data[-1]

            func(phone_number)
            phones = saves[2]

            response = "END Thank you for using HealthRadar\n"
            response += "Data for {} has been captured \n".format(phones)
            response += "Remember to call NCDC on \n"
            response += "0800 9700 0010 if you suspect COVID-19."

        # elif len(text.split("*")) ==2 and text.split('*')[0] == '2':

    except IndexError as e:
        print(e)
        response = "END Wrong response recieved"

    resp = make_response(response, 200)
    resp.headers["Content-type"] = "text/plain"
    return resp
