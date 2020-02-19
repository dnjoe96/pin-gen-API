from flask import jsonify, request
from app import app, mongo
from app.models import send_message


@app.route('/activate', methods=['PUT'])
def activate_card():
    request_data = request.get_json()

    """ requesting serial number """
    serial_no = request_data['serial_no']
    category = request_data['category']

    """ connecting to database """
    try:
        mongo_data = mongo.db.pin_data
    except ConnectionError as e:
        return jsonify({'message': 'network error, check internet connection'})

    find = mongo_data.find_one({'serial_no': serial_no})

    """ checking if serial number is valid """
    if not find:
        return jsonify({'message': 'Invalid serial number'})

    """ check category that has been selected and select the range and append in a list """
    if category == 1:
        ser = list(range(serial_no, serial_no + 10))
    elif category == 2:
        ser = list(range(serial_no, serial_no + 100))
    elif category == 3:
        ser = list(range(serial_no, serial_no + 1000))
    elif category == 4:
        ser = list(range(serial_no, serial_no + 10000))
    elif category == 0:
        ser = [serial_no]

    serial_set = []
    for serial_number in ser:

        """ check for each serial number """
        find1 = mongo_data.find_one({'serial_no': int(serial_number)})
        if find1:
            if find1['activation_status'] == 0:

                """ activate card """
                mongo_data.update_one({'serial_no': int(serial_number)}, {"$set": {"activation_status": 1}})
                serial_set.append(serial_number)

        else:
            break

    """ counting the number of cards that has been activated """
    num = len(serial_set)

    if num > 0:
        """ calling a function to send SMS response to the user, getting the contact details of the owner of the card """
        send_message('+2348121704437', num, serial_set)

        if num == 1:
            return jsonify({'message': '{} card Activated'.format(num) + ' ' + 'serial number: {}'.format(serial_set[0])})
        else:
            return jsonify({'message': '{} cards Activated'.format(num), 'range': 'from {} to {}'.format(serial_set[0], serial_set[-1])})

    else:
        return jsonify({'message': 'card(s) already activated'})