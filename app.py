from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import os
import json

app = Flask(__name__)

# --- Google Sheets Setup ---
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_CREDENTIALS = os.getenv('GOOGLE_CREDENTIALS')
SPREADSHEET_ID = os.getenv('1BCEnSKZVoDX8AoyWLLiNErcv4k3hVAj767SZ77eypXE')

info = json.loads(GOOGLE_CREDENTIALS)
creds = service_account.Credentials.from_service_account_info(info, scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)


# --- Log to Google Sheets ---
def log_to_sheets(phone_number, answer):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    body = {
        'values': [[phone_number, answer, timestamp]]
    }
    sheets_service.spreadsheets().values().append(
        spreadsheetId=1BCEnSKZVoDX8AoyWLLiNErcv4k3hVAj767SZ77eypXE,
        range='Sheet1!A1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    print(f"✅ Logged to sheet: {phone_number}, {answer}, {timestamp}")


# --- Twilio Voice Entry Point ---
@app.route("/voice", methods=['POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(input='speech', timeout=5, num_digits=1, action='/gather')
    gather.say("Hi, this is an AI agent calling on behlaf of Mr Kennedy, are you in pain from the recenlt operation?")
    response.append(gather)
    response.redirect('/voice')
    return Response(str(response), mimetype='application/xml')


# --- Twilio Speech Capture ---
@app.route("/gather", methods=['POST'])
def gather():
    speech_result = request.form.get('SpeechResult', '(no speech)')
    caller = request.form.get('From', '(unknown)')
    print(f"📞 Call from {caller} — heard: {speech_result}")
    log_to_sheets(caller, speech_result)

    response = VoiceResponse()
    response.say("Thank you. Your response has been recorded and reported to Mr Kennedy. Have a nice weekend!!!!")
    response.hangup()
    return Response(str(response), mimetype='application/xml')


if __name__ == '__main__':
    app.run(debug=True)
