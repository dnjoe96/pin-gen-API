


from twilio.rest import Client

account_sid = 'ACbcaa07eb1cef77d9ed6bf618135750ce'
auth_token = 'a8bb36e4d86168cf370d70fd99612a25'
client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Hello! This is an editable text message. You are free to change it and write whatever you like.',
    to='whatsapp:+2348121704437'
)

print(message.sid)



