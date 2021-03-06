#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):

    #img_base = "https://raw.githubusercontent.com/svet4/faq-sample/master/img/"

    if req.get("result").get("action") == "topics.authentication":
    
        speech = "You can find your *authentication tokens* in your agent settings > General > API Keys. \n Read more here: https://docs.api.ai/docs/authentication."

        #pic_url = img_base + "access_tokens.png"

        print("Response:")
        print(speech)

        slack_message = {
        "text": speech,
        "attachments": [
            {
                "text": "To go to your agent settings, click on the gear button:",
                "image_url": "https://raw.githubusercontent.com/svet4/faq-sample/master/img/access_tokens.png"
            }
        ]
        }


        return {
        #"speech": speech,
        #"displayText": speech,
        "data": {"slack": slack_message},
        # "contextOut": [],
        "source": "apiai-support-bot"
    }

    else:
        return {}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
