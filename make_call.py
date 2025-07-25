from twilio.rest import Client

account_sid = 'ACb518174d372a2b73829123cc13158ffd'
auth_token = '0c38f1324f49979c376c4109c9d20e06'
client = Client(account_sid, auth_token)

call = client.calls.create(
    url='https://patient-caller-bot.onrender.com/voice',
    to='+61490081545',  # Patient's phone number
    from_='+61490081545'  # Your Twilio number
)

print(f"Calling... SID: {call.sid}")


# from twilio.rest import Client

# # Replace with your actual Twilio account credentials
# account_sid = 'YOUR_ACCOUNT_SID'
# auth_token = 'YOUR_AUTH_TOKEN'
# client = Client(account_sid, auth_token)

# # Your Twilio number and your test number (must be verified if on trial account)
# from_number = '+1XXXXXXXXXX'  # Your Twilio number
# to_number = '+61XXXXXXXXX'    # Your phone number (Australia format in your case)

# # Public endpoint to your voice bot (e.g. Render or Ngrok)
# voice_url = 'https://your-app.onrender.com/voice'

# # Create and make the call
# call = client.calls.create(
#     to=to_number,
#     from_=from_number,
#     url=voice_url
# )

# print(f"✅ Call initiated! SID: {call.sid}")
