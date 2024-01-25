import json
import requests

from thoughtspot_rest_api_v1 import *

username = 'username'
password = 'password'
server = 'https://{instance}.thoughtspot.cloud'

# Create TSRestApiV2 object to do all the requests
ts: TSRestApiV2 = TSRestApiV2(server_url=server)
# Try to request token from /auth/token/full and then use token to be the bearer_token of the TSRestApiV2 obj
try:
    auth_token_response = ts.auth_token_full(username=username, password=password, validity_time_in_sec=3000)
    ts.bearer_token = auth_token_response['token']
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    print("Exiting script after error...")
    exit()

# Create request to /metadata/search to find the Liveboards and Answers matching the name pattern
# Use the Playground to build your request, then copy/paste in the script
search_request = {
    "metadata": [
    {
      "name_pattern": "%QA%",
      "type": "LIVEBOARD"
    },
    {
      "name_pattern": "%QA%",
      "type": "ANSWER"
    }
  ],
    'record_offset': 0,
    'record_size': 100000
}

# Create a List to populate with the IDs of the objects to share to the group
ids_to_update = []

try:
    # Send request to /metadata/search endpoint
    resp = ts.metadata_search(request=search_request)
    # Iterate through the results from the API response to double-check that the name value matches exactly
    for item in resp:
        m_name = item["metadata_name"]
        m_id = item["metadata_id"]
        if m_name.find("QA ") != -1:
            ids_to_update.append(m_id)  # Get final List of IDs to send
    print("Found the following metadata items to update:")
    print(ids_to_update)
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

# Check if group exists, create if not
group_name = "QA"
# Create the request body for /groups/create endpoint
groups_request = {
    "group_identifier": group_name
}

try:
    # Use /groups/search endpoint to see if group already exists with the expected name
    resp = ts.groups_search(request=groups_request)
    # If it does not exist, create the group
    if len(resp) == 0:
        # Create the request body for /groups/create endpoint (use Playground, then substitute variables)
        group_create_req = {
          "name": group_name,
          "display_name": group_name,
          "type": "LOCAL_GROUP",
          "visibility": "SHARABLE"
        }
        # Send the request to /groups/create
        create_resp = ts.groups_create(request=group_create_req)
        # Retrieve the GUID for the newly created Group from the response
        group_id = create_resp['id']
    else:
        # There should only be one result in the list
        group_id = resp[0]['id']

    # Share all content with the QA group
    # Create the request body for /security/metadata/share in the Playground, then substitute variables
    share_req = {
        "metadata_identifiers": ids_to_update,
        "permissions": [
            {
                "principal": {
                    "identifier": group_id
                },
                "share_mode": "READ_ONLY"
            }
        ],
        "emails": [],
        "message": "",
        "enable_custom_url": False
    }

    # Use security/metadata/share endpoint
    share_resp = ts.security_metadata_share(request=share_req)
    print(json.dumps(share_resp, indent=2))

except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    # Check for a particular 400 error, which previous versions of API did when exact match not found
    print(e.response.content)
    print("Exiting script due to API error...")
    exit()



