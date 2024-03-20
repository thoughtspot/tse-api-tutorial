import requests
import json

thoughtspot_url = 'https://training.thoughtspot.cloud'
org_id = 1613534286
api_version = '2.0'
base_url = '{thoughtspot_url}/api/rest/{version}/'.format(thoughtspot_url=thoughtspot_url, version=api_version)
api_headers = {
    'X-Requested-By': 'ThoughtSpot', 
    'Accept': 'application/json'
}

requests_session = requests.Session()
# Set the headers for all uses of the requests_session object
requests_session.headers.update(api_headers)

# url is base_url + endpoint
endpoint = "auth/token/full"
url = base_url + endpoint

# JSON request as Python Dict
json_post_data = {
  "username": "user251",
  "validity_time_in_sec": 3000,
  "org_id": org_id,
  "auto_create": False,
  "password": "Embedding2024!"
}

try:
    # requests returns back Response object with various properties and methods
    resp = requests_session.post(url=url, json=json_post_data)
    # This method causes Python Exception to throw if the response status is not 2XX
    resp.raise_for_status()
    # Retrieve the JSON body of response and convert into Python Dict
    # If a call (like a DELETE) returns 204 instead of 200, with no body, this may cause error
    resp_json = resp.json()
    # You can just print(resp_json) to see the Python Dict
    print(json.dumps(resp_json, indent=2))
except requests.exceptions.HTTPError as e:
    print("Requests")
    print(e)
    print(e.request)
    print(e.request.url)
    print(e.request.headers)
    print(e.request.body)
    print(e.response.content)

print(resp_json["token"])