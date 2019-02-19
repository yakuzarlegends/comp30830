import requests
import scraping.key as key
import json


API_KEY = key.KEY
URL = f"api.jcdecaux.com/vls/v1/stations?contract=Dublin&apiKey={API_KEY}"

response = requests.get(url, verify=True)

if (response.ok):
    jData = json.loads(response.content)
    print("The response contains {0} properties".format(len(jData)))
    print("\n")
    for i in jData:
        print i + " : " + jData[i]
else:
  # If response code is not ok (200), print the resulting http error code with description
    response.raise_for_status()
