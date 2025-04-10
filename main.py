import flask
from flask import request, Flask, jsonify
import logging
from flask_cors import CORS
import os
import json
from thefuzz import process, fuzz

app = Flask(__name__)
CORS(app)
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.post("/samplewh")
def sample_wh(optional_param=None):
  if optional_param:
    print(f"optional_param {optional_param}")
  data = request.get_json()
  print(f"data {data}")
  logging.warning(f"data {data}")

  # It cames from Playbook
  if 'hotelName' in data:
    logging.warning(" 'hotelName' key in JSON data.")
    hotel_name = data['hotelName']
    print(" 'hotelName' key in JSON data.")
    logging.warning(f"hotel_name {hotel_name}")
    print (f"hotel_name {hotel_name}")

    known_hotels = [
        "Gran Meliá Palacio de Isora",
        "Gran Meliá Fenix"
    ]
    best_match_partial, score_partial = process.extractOne(hotel_name, known_hotels, scorer=fuzz.partial_ratio)
    logging.warning(f"match {best_match_partial}")
    if best_match_partial == "Gran Meliá Fenix":
        phoneNumber = " 123"
    else:
        phoneNumber = " 456"


    output = {
        "phoneNumber": f"El telefono de {best_match_partial}  es {phoneNumber}"
        }
    response_json = json.dumps(output)
    return response_json







  # It cames from flow
  hotel_name = data['sessionInfo']['parameters']["hotel_name"]
  if hotel_name == "Gran Meliá Fenix":
    phoneNumber = " 123"
  else:
    phoneNumber = " 456"

  output = {
    'sessionInfo': {
      'parameters': {
        'userAuthenticated': 'y',
        }
      },
    "fulfillment_response": {
      "messages": [
        {
          "text": {
            "text": [f"El telefono de {hotel_name} es {phoneNumber}"]
            }
        },
        {
          "payload": {
            "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    { "text": "Option 1" },
                                    { "text": "Option 2" },
                                    { "text": "Option 3" }
                                ]
                            }
                        ]
                    ]

          }

        }
      ]
    }
  }
  response_json = json.dumps(output)
  return response_json
  # return flask.jsonify({"results": "output"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
