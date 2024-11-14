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
    auth_token_response = ""
    ts.bearer_token = ""
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
}

try:
    # Send request to /metadata/search endpoint
    metadata_resp = ""
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

# Create List to hold the final set of Answers + Liveboards we want to tag and share,
final_list_of_objs =[]

# Iterate through the results from the API response to double-check that the name value matches exactly
for item in metadata_resp:
    m_name = ""
    m_id = ""
    # Python string find is Case-Sensitive 
    if m_name.find("(Sample)") != -1:
       pass # We'll add the whole object to the new List

# 2. Add a tag to each item called 'Tutorial Test'

# Get the ID of the tag called 'Tutorial Test'
#   What if there is no tag called 'Tutorial Test'?


#
# Find the Tag Identifer so we can assign
# Create new Tag if it doesn't exist
#
try:
    tags = ""
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

if len(tags) == 0:
    try:
        new_tag = ""
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
        pass

   assign_req = {

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


#
# Find the Group Identifer so we can share
# Create new Group if it doesn't exist
#


# 3.2 Share content as READ-ONLY to the group

#
