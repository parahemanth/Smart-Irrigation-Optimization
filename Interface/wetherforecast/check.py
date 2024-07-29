import requests
import json

website = "https://api.thingspeak.com/channels/2313573/feeds.json?api_key=QJAOBTVSDCMS21YI&results=2"
response = requests.get(website)

if response.status_code == 200:
    data = json.loads(response.text)

    # Access field1 and field2 values from the JSON data
    field1_values = [feed['field1'] for feed in data['feeds']]
    field2_values = [feed['field2'] for feed in data['feeds']]

    print(field1_values)
    print(field2_values)
else:
    print("Failed to retrieve data. Status code:", response.status_code)
