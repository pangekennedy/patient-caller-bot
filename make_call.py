import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")

if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
    raise Exception("Missing one or more Twilio environment variables.")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def make_call(to_number):
    call = client.calls.create(
        to=to_number,
        from_=TWILIO_FROM_NUMBER,
        url="https://patient-caller-bot-active.onrender.com/voice"  # Replace with your actual URL
    )
    print(f"Call initiated: SID {call.sid}")

if __name__ == "__main__":
    # Hardcoded number here (must be in E.164 format, e.g. +61412345678)
    patient_number = "+61490081545"
    make_call(patient_number)


# import os
# from dotenv import load_dotenv
# from twilio.rest import Client

# # Load local .env variables (for Twilio keys)
# load_dotenv()

# TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
# TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")  # Your Twilio phone number

# if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
#     raise Exception("Missing one or more Twilio environment variables.")

# client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# def make_call(to_number):
#     call = client.calls.create(
#         to=to_number,
#         from_=TWILIO_FROM_NUMBER,
#         url="https://your-app.onrender.com/voice"  # Replace with your actual deployed URL
#     )
#     print(f"Call initiated: SID {call.sid}")

# if __name__ == "__main__":
#     patient_number = input("+61490081545")
#     make_call(patient_number)


# from twilio.rest import Client
# import os
# from dotenv import load_dotenv

# load_dotenv()

# account_sid = os.getenv("TWILIO_ACCOUNT_SID")
# auth_token = os.getenv("TWILIO_AUTH_TOKEN")

# client = Client(account_sid, auth_token)

# call = client.calls.create(
#     url='https://patient-caller-bot-active.onrender.com/voice',
#     to='+61490081545',  # Patient's phone number
#     from_='+16088796871'  # Your Twilio number
# )

# print(f"Calling... SID: {call.sid}")


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
