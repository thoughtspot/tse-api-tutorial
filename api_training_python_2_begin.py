import json
import requests

from thoughtspot_rest_api_v1 import *

username = 'username'
password = 'password'
server = 'https://{instance}.thoughtspot.cloud'
org_id = 1613534286

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
search_answers_request = {
}

search_liveboards_request = {

}

# Create Lists to hold the final set of Answers + Liveboards we want to request SQL from (this isn't required)
answers_to_find_sql = []
lbs_to_find_sql =[]

try:
    # Send request to /metadata/search endpoint
    
    # Iterate through the results from the API response to double-check that the name value matches exactly
    for item in answers_resp:

      # Add the whole object if it matches to the answers_to_find_sql list
        
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

    # Iterate through the results from the API response to double-check that the name value matches exactly
    for item in lbs_resp:

        # Add the whole object to the lbs_to_find_sql list

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


        # Print out the sql_resp structure to inspect for the details you want to retrieve
        # print(json.dumps(sql_resp, indent=2))

        # Answers only will ever have one sql_query 
        sql_query = 
        answer_id = 
        answer_name = 
        # Display the information about the Answer and then the query
        print("".format(answer_id, answer_name))
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

        lb_id = 
        lb_name = 

        # Display the information about the Liveboard before iterating through the visualizations for their details
        print("".format(lb_id, lb_name))
        print("---- ")

        # Liveboards have visualizations each with their own query, iterate through each query to find the details
        for sql_query in sql_resp['sql_queries']:
            
            viz_id = 
            viz_name = 
            query = 

            # Display the information about the Viz and then the query
            print("".format(viz_id, viz_name))
            print(query)
            print("---- ")
        print("")

    except requests.exceptions.HTTPError as e:
        print("Error from the API: ")
        print(e)
        print(e.response.content)
        print(e.request.body)
        exit() 