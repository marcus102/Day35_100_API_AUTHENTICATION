#Note! For the code to work you need to replace all the placeholders with
#Your own details. e.g. account_sid, lat/lon, from/to phone numbers.

import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
api_key = os.environ.get("77bdb6ff02c171ac7d0e3678999c59a1")
account_sid = "AC5e121a66d2536267703454d8b8828d03"
auth_token = os.environ.get("c3ebf1ec95ade46906d4e160b7249eb0")

weather_params = {
    "lat": "8.905540",
    "lon": "7.187090",
    "appid": '77bdb6ff02c171ac7d0e3678999c59a1',
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages \
        .create(
            body="It is going to rain today.",
            from_='+13156286894',
            to='+2349064663629'
            )
    print(message.status)
