from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import search

# export FLASK_APP
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Get the message the user sent
    body = request.values.get('Body')
    params = body.split()

    # Start TwiML response
    resp = MessagingResponse()

    # Add the message
    if params[0].lower() == 'google':
        result = search.googleSearch(body[7:])
        resp.message("Here is Google's top result:\n" + result)
    elif params[0].lower() == 'translate':
        if len(params) >= 3:
            msg = search.translate(" ".join(params[2:]), params[1].lower())
            if msg == "":
                resp.message("An error occurred during translation.")
            else:
                resp.message(msg)
        else:
            resp.message("Send a message in the following format: 'translate CODE TEXT' where "
                         "CODE is the ISO 639-1 code for the language wanted ("
                         "found at http://www.loc.gov/standards/iso639-2/php/code_list.php) "
                         "and TEXT is the message to be translated.")
    elif params[0].lower() == 'wiki':
        result = search.wikiSearch(body[5:])
        if len(result) < 1530:
            resp.message("Information from Wikipedia:\n" + result)
        else:
            resp.message("Information from Wikipedia:\n" + result[:1525])
            result = result[1525:]
            while len(result) >= 1530:
                resp.message(result[:1525])
                result = result[1525:]
            resp.message(result)
    else:
        resp.message("The Robots are coming! Head for the hills!")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
