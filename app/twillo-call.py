# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


# Your Account Sid and Auth Token from twilio.com/console
# DANGER! This is insecure. See http://twil.io/secure
account_sid = 'ACbcaa07eb1cef77d9ed6bf618135750ce'
auth_token = os.environ.get('TWILIO_TOKEN')

client = Client(account_sid, auth_token)

call = client.calls.create(
                        twiml='<Response><Say>This is a very interesting way to start the week</Say></Response>',
                        to='+2348121704437',
                        from_='+17177272510'
                    )

print(call.sid)



'''
my twilio phone number = +17177272510
'''