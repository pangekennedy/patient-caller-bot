from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Main entry point for the voice call
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/gather', method="POST")
    gather.say("Hi, this is a representative calling on behalf of Mr Kennedy. Are you experiencing any pain today? Press 1 for yes. Press 2 for no.")
    response.append(gather)
    response.redirect('/voice')  # Repeats the question if no input
    return str(response)

from flask import request

@app.route("/gather", methods=['GET', 'POST'])
def gather():
    digit = request.values.get('Digits')
    caller = request.values.get('From')
    response = VoiceResponse()

    if digit == '1':
        response.say("Thank you. We'll notify Mr Kennedy.")
        log_response("Yes", caller)
    elif digit == '2':
        response.say("Great. Take care and have a nice weekend.")
        log_response("No", caller)
    else:
        response.say("Sorry, I didn’t understand that.")
        response.redirect('/voice')

    return str(response)


# Process patient response (without the DB)
# @app.route("/gather", methods=['GET', 'POST'])
# def gather():
#     digit = request.values.get('Digits')
#     response = VoiceResponse()

#     if digit == '1':
#         response.say("Thank you. We’ll notify your Mr Kennedy.")
#         log_response("Yes")
#     elif digit == '2':
#         response.say("Great. Take care and have a nice day.")
#         log_response("No")
#     else:
#         response.say("Sorry, I didn’t understand that.")
#         response.redirect('/voice')
    
#     return str(response)

# # Simulate response logging (replace with DB later)
# def log_response(answer):
#     with open("responses.txt", "a") as f:
#         f.write(f"Patient response: {answer}\n")

import datetime
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load Google Sheets credentials (use a Render secret or env var in production)
# SERVICE_ACCOUNT_FILE = 'your-service-account-file.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = 'Tiwilio Patient Responses'
SHEET_NAME = 'Sheet1'

# credentials = service_account.Credentials.from_service_account_file(
#     SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

import json
from google.oauth2 import service_account

google_credentials = os.environ.get('google_credentials')

info = json.loads(google_credentials)
credentials = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)

def log_response(response, phone_number):
    sheet = service.spreadsheets()
    values = [[
        datetime.datetime.now().isoformat(),
        phone_number,
        response
    ]]
    body = {'values': values}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f'{SHEET_NAME}!A:C',
        valueInputOption='USER_ENTERED',
        body=body
    ).execute()


if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
