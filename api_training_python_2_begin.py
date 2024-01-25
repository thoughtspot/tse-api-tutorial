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

except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    print("Exiting script after error...")
    exit()

# Create request to /metadata/search to find the Liveboards and Answers matching the name pattern
# Use the Playground to build your request, then copy/paste in the script
search_request = {

}

# Create a List to populate with the IDs of the objects to share to the group
ids_to_update = []

try:
    # Send request to /metadata/search endpoint

    # Iterate through the results from the API response to double-check that the name value matches exactly

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
}

try:
    # Use /groups/search endpoint to see if group already exists with the expected name

    # If it does not exist, create the group
    if len(resp) == 0:
        # Create the request body for /groups/create endpoint (use Playground, then substitute variables)
        group_create_req = {

        }
        # Send the request to /groups/create

        # Retrieve the GUID for the newly created Group from the response

    else:
        # There should only be one result in the list
        group_id = resp[0]['id']

    # Share all content with the QA group
    # Create the request body for /security/metadata/share in the Playground, then substitute variables
    share_req = {

    }

    # Use security/metadata/share endpoint

    print(json.dumps(share_resp, indent=2))

except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    # Check for a particular 400 error, which previous versions of API did when exact match not found
    print(e.response.content)
    print("Exiting script due to API error...")
    exit()



