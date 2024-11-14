import json
import requests

from thoughtspot_rest_api_v1 import *

username = '{}'
password = '{}'
server = 'https://{}.thoughtspot.cloud'
org_id = 1613534286

# Create TSRestApiV2 object to do all the requests
ts: TSRestApiV2 = TSRestApiV2(server_url=server)
# Try to request token from /auth/token/full and then use token to be the bearer_token of the TSRestApiV2 obj
try:
    auth_token_response = ts.auth_token_full(username=username, password=password, validity_time_in_sec=3000, org_id=org_id)
    ts.bearer_token = auth_token_response['token']
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    print("Exiting script after error...")
    exit()

# 1. Find all Liveboards and Answers with a name that includes '(Sample)'

# Get all of the items with name '(Sample)'
#  Is this a case-sensitive or insensitive operation? Are we finding anywhere in the name or just at start or end?

# Create request to /metadata/search to find the Liveboards and Answers matching the name pattern
# Use the Playground to build your request, then copy/paste in the script
search_request = {
    "metadata": [
    {
      "name_pattern": "(Sample)",
      "type": "ANSWER"
    },
    {
      "name_pattern": "Sample)",
      "type": "LIVEBOARD"
    }
  ],
    'record_offset': 0,
    'record_size': 10000
}

try:
    # Send request to /metadata/search endpoint
    metadata_resp = ts.metadata_search(request=search_request)
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

# Create List to hold the final set of Answers + Liveboards we want to tag and share,
final_list_of_objs =[]

# Iterate through the results from the API response to double-check that the name value matches exactly
for item in metadata_resp:
    m_name = item["metadata_name"]
    m_id = item["metadata_id"]
    # Python string find is Case-Sensitive 
    if m_name.find("(Sample)") != -1:
        final_list_of_objs.append(item)  # We'll add the whole object to the new List

# 2. Add a tag to each item called 'Tutorial Test'

# Get the ID of the tag called 'Tutorial Test'
#   What if there is no tag called 'Tutorial Test'?


#
# Find the Tag Identifer so we can assign
# Create new Tag if it doesn't exist
#
try:
    tags = ts.tags_search(tag_identifier="Tutorial Test")
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

if len(tags) == 0:
    try:
        new_tag = ts.tags_create(name="Tutorial Test")
        tag_id = new_tag['id']
    except requests.exceptions.HTTPError as e:
        print("Error from the API: ")
        print(e)
        print(e.response.content)
        exit()
else:
    tag_id = tags[0]['id']

# Assign the tag to the items

try:
   # When we copied from the Playground, we realize the format of the `metadata` section is an Array of Objects,
   # which needs to be a List of Dicts in Python syntax [ {"identifier": metadata_id}, ...]
   
   tag_metadata_section = []
   # Iterate through each object and make the Dict in create format
   for obj in final_list_of_objs:
        tag_metadata_section.append({"identifier" : obj['metadata_id']})

   assign_req = {
        "metadata": tag_metadata_section,
        "tag_identifiers": [tag_id]
   }

   assign_resp = ts.tags_assign(requst=assign_req)
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

#
# Extra credit assigment below:
#

# 3. Give read-only access to a 'Tutorial Test' group

# 3.1 Get the ID of the group called 'Tutorial Test'
#  Is 'Tutorial Test' the name or the display_name property?
#  What if there is no group called 'Tutorial Test'?
try:
    # Copy from Playground
    groups_req = {
        "record_offset": 0,
        "record_size": 10,
        "group_identifier": "Tutorial Test"
    }
    groups = ts.groups_search(request=groups_req)
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

#
# Find the Group Identifer so we can share
# Create new Group if it doesn't exist
#
if len(groups) == 0:
    try:
        group_create_req = {
            "name": "Tutorial Test",
            "display_name": "Tutorial Test",
            "type": "LOCAL_GROUP",
            "visibility": "NON_SHARABLE"
        }
        new_group = ts.groups_create(request=group_create_req)
        group_id = new_group['id']
    except requests.exceptions.HTTPError as e:
        print("Error from the API: ")
        print(e)
        print(e.response.content)
        exit()
else:
    group_id = groups[0]['id']

# 3.2 Share content as READ-ONLY to the group

#
final_metadata_ids = []
for obj in final_list_of_objs:
    final_metadata_ids.append(obj['metadata_id'])

try:    
    share_req = {
        "permissions": [
            {
            "principal": {
                "identifier": group_id
            },
            "share_mode": "READ_ONLY"
            }
        ],
        "message": "N/A",
        "enable_custom_url": False,
        "notify_on_share":False,
        "has_lenient_discoverability": False,
        "metadata_identifiers": final_metadata_ids
    }
    share_resp = ts.security_metadata_share(request=share_req)

except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()
