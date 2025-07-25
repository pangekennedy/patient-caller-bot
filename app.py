from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Main entry point for the voice call
@app.route("/voice", methods=['GET', 'POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(num_digits=1, action='/gather', method="POST")
    gather.say("Hi, this is your clinic. Are you experiencing any pain today? Press 1 for yes. Press 2 for no.")
    response.append(gather)
    response.redirect('/voice')  # Repeats the question if no input
    return str(response)

# Process patient response
@app.route("/gather", methods=['GET', 'POST'])
def gather():
    digit = request.values.get('Digits')
    response = VoiceResponse()

    if digit == '1':
        response.say("Thank you. We’ll notify your doctor.")
        log_response("Yes")
    elif digit == '2':
        response.say("Great. Take care and have a nice day.")
        log_response("No")
    else:
        response.say("Sorry, I didn’t understand that.")
        response.redirect('/voice')
    
    return str(response)

# Simulate response logging (replace with DB later)
def log_response(answer):
    with open("responses.txt", "a") as f:
        f.write(f"Patient response: {answer}\n")

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
