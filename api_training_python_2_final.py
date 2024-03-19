import json
import requests

from thoughtspot_rest_api_v1 import *

username = '{}}'
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

# Create request to /metadata/search to find the Liveboards and Answers matching the name pattern
# Use the Playground to build your request, then copy/paste in the script
search_answers_request = {
    "metadata": [
    {
      "name_pattern": "%QA%",
      "type": "ANSWER"
    }
  ],
    'record_offset': 0,
    'record_size': 100000
}

search_liveboards_request = {
 "metadata": [
    {
      "name_pattern": "%QA%",
      "type": "LIVEBOARD"
    }
  ],
    'record_offset': 0,
    'record_size': 100000
}

# Create Lists to hold the final set of Answers + Liveboards we want to request SQL from (this isn't required)
answers_to_find_sql = []
lbs_to_find_sql =[]

try:
    # Send request to /metadata/search endpoint
    answers_resp = ts.metadata_search(request=search_answers_request)
    # Iterate through the results from the API response to double-check that the name value matches exactly
    for item in answers_resp:
        m_name = item["metadata_name"]
        m_id = item["metadata_id"]
        if m_name.find("QA ") != -1:
            answers_to_find_sql.append(item)  # We'll add the whole object to the new list
    # print("Found the following Answers to request from:")
    # print(json.dumps(answers_to_find_sql, indent=2))
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()


# Repeat steps above, but for the Liveboards response
try:
    # Send request to /metadata/search endpoint
    lbs_resp = ts.metadata_search(request=search_liveboards_request)
    # Iterate through the results from the API response to double-check that the name value matches exactly
    for item in lbs_resp:
        m_name = item["metadata_name"]
        m_id = item["metadata_id"]
        if m_name.find("QA ") != -1:
            lbs_to_find_sql.append(item)  # We'll add the whole object to the new list
    # print("Found the following Liveboards to request from:")
    # print(json.dumps(lbs_to_find_sql, indent=2))
except requests.exceptions.HTTPError as e:
    print("Error from the API: ")
    print(e)
    print(e.response.content)
    exit()

#
# Retrieve and Display all of the SQL queries
# Here you might make decisions about what to show, format of display
#

for answer in answers_to_find_sql:
    try:
        # metadata_answer_sql doesn't have generic request, it lets you pass in answer_identifier directly
        sql_resp = ts.metadata_answer_sql(answer_identifier=answer['metadata_id'])

        # Print out the sql_resp structure to inspect for the details you want to retrieve
        # print(json.dumps(sql_resp, indent=2))

        # Answers only will ever have one sql_query 
        sql_query = sql_resp['sql_queries'][0]['sql_query']
        answer_id = sql_resp['metadata_id']
        answer_name = sql_resp['metadata_name']
        # Display the information about the Answer and then the query
        print("Answer:\n{}\n{}\n".format(answer_id, answer_name))
        print(sql_query)
        print("---- \n")
    except requests.exceptions.HTTPError as e:
        print("Error from the API: ")
        print(e)
        print(e.response.content)
        exit() 

# Retrieve the SQL of each Liveboard
for lb in lbs_to_find_sql:
    try:
        # metadata_liveboard_sql doesn't have generic request, it lets you pass in liveboard_identifier directly
        sql_resp = ts.metadata_liveboard_sql(liveboard_identifier=lb['metadata_id'])

        lb_id = sql_resp['metadata_id']
        lb_name = sql_resp['metadata_name']

         # Display the information about the Liveboard before iterating through the visualizations for their details    
        print("Liveboard:\n{}\n{}\n".format(lb_id, lb_name))
        print("---- ")
        
        # Liveboards have visualizations each with their own query
        for sql_query in sql_resp['sql_queries']:
            
            viz_id = sql_query['metadata_id']
            viz_name = sql_query['metadata_name']
            query = sql_query['sql_query']

            print("Viz:\n{}\n{}\n".format(viz_id, viz_name))
            print(query)
            print("---- ")
        print("")

    except requests.exceptions.HTTPError as e:
        print("Error from the API: ")
        print(e)
        print(e.response.content)
        print(e.request.body)
        exit() 