from flask import request, make_response
import requests, json
from app import app


def ussd_proceed(response):
    return "CON {}".format(response)


def ussd_stop(response):
    return "END {}".format(response)


def get_pin():
    response = "Welcome to HealthRadar\n"
    response += "Enter Please enter PIN to verify\n"
    return ussd_proceed(response)


def display_menu():
    # main menu
    response = "Welcome to HealthRadar\n"
    response += "Enter patient phone number to begin\n"
    return ussd_proceed(response)


def first_menu():
    response = "Select symptoms\n"
    response += "1. Fever\n"
    response += "2. Dry cough\n"
    response += "3. Myalgia_or_Arthralgia\n"
    response += "4. Fatgue\n"
    response += "5. Sputum production\n"
    response += "6. Shortness of breath\n"
    response += "7. Sore throat\n"
    response += "8. Headache\n"
    response += "9. Chills\n"
    response += "0. More Symptoms\n"
    response += "00. Submit"
    return ussd_proceed(response)


def second_menu():
    response = "Select symptoms\n"
    response += "1. Fever\n"
    response += "2. Dry cough\n"
    response += "3. Myalgia_or_Arthralgia\n"
    response += "4. Fatgue\n"
    response += "5. Sputum production\n"
    response += "6. Shortness of breath\n"
    response += "7. Sore throat\n"
    response += "8. Headache\n"
    response += "9. Chills\n"
    response += "0. More Symptoms\n"
    response += "00. Submit"
    return ussd_proceed(response)


def third_menu():
    response = "Select symptoms\n"
    response += "1. Diarrhea\n"
    response += "2. Nasal congestion\n"
    response += "3. Nause or vomiting\n"
    response += "4. Hemoptysis\n"
    response += "5. Conjuntival\n"
    response += "6. Meningitis\n"
    response += "7. Constipation\n"
    response += "8. Chest_pain\n"
    response += "9. Abdominal_Pain\n"
    response += "00. Submit"
    return ussd_proceed(response)


API_KEY = 'healthradar-95302420205yeeyqz'


@app.route('/ussd', methods=['GET', 'POST'])
def ussd():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber",None)
    # phone_number = '+2349018858924'
    text = request.values.get("text", "default")

    def_symptoms = ["fever", "dry_cough", "myalgia_or_arthralgia", "fatgue", "sputum_production",
                    "shortness_of_breath", "sore_throat", "headache", "chills", "diarrhea", "nasal_congestion",
                    "nausea_or_vomiting", "hemoptysis", "conjuntival", "meningitis", "constipation", "chest_pain",
                    "abdominal_pain"]
    symptoms = []
    data = []

    def func():
        global phone
        # print(data)
        save = data[-1]
        selection = []
        phone = save[1]

        for one in save:
            if len(one) != 11 and one != '0' and one != '00':
                selection.append(one)

        selections = selection[1:]

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
        patient_number = phone
        provider_number = '0' + phone_number[4:]
        payloads = {"patient_number": patient_number, "provider_number": provider_number, "symptoms": final_symptoms}
        print(payloads)

        requests.post("https://health-radar.herokuapp.com/api/patients", data=payloads)

    # the phone number to pass into the Response

    if text == "":
        response = get_pin()

    elif len(text) == 4:

        pin = text.split("*")[0]

        phones = '0' + phone_number[4:]

        request_headers = {"Authorization": API_KEY}
        payload = {"phone": phones, "PIN": pin}
        print(payload)
        r = requests.post('https://healthradarapp.herokuapp.com/api/v1/user/verify', data=payload,
                          headers=request_headers)

        print(json.loads(r.content)['success'])

        if json.loads(r.content)['success'] == False:
            response = "END Thank you for using HealthRadar\n"
            response += "You have entered an invalid number."
        else:
            response = display_menu()

    elif len(text.split("*")[1]) == 11 and len(text.split('*')) == 2:
        save = text.split('*')[1]
        data.append(save)
        print(save)

        # this layer ensures that the phone number is correct, else error
        if len(text.split("*")[1]) == 11:
            response = first_menu()
        else:
            response = "END Thank you for using HealthRadar\n"
            response += "You have entered an invalid number."

    elif text.split('*')[-1] != '0' and text.split('*')[-1] != '00':
        save = text.split('*')
        data.append(save)
        print(save)

        # this layer ensures that the phone number is correct, else error
        if len(text.split("*")[1]) == 11:
            response = second_menu()
        else:
            response = "END Thank you for using HealthRadar\n"
            response += "You have entered an invalid number."

    elif text.split('*')[-1] == '0':
        save = text.split('*')
        data.append(save)
        print(save)
        response = third_menu()

    elif text.split('*')[-1] == '00':
        save = text.split('*')
        data.append(save)
        print(save)
        func()
        saves = data[-1]
        phones = saves[0]
        response = "END Thank you for using HealthRadar\n"
        response += "Data for {} has been captured \n".format(phones)
        response += "Remember to call NCDC on \n"
        response += "0800 9700 0010 if you suspect COVID-19."

    resp = make_response(response, 200)
    resp.headers["Content-type"] = "text/plain"
    return resp
