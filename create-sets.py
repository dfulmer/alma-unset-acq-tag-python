import requests
import json
from dotenv import dotenv_values

# This script creates an itemized set by combining the two sets: OCLC_every_physical_title_with_acquisition_v2 NOT OCLC_every_physical_title_except_acquisition_v2.
# The combined set which results consists of all acq-only Physical Titles in Alma.
# OCLC_every_physical_title_with_acquisition_v2 Set ID 34493393360006381
# OCLC_every_physical_title_except_acquisition_v2 Set ID 22766924310006381
# OCLC_every_physical_title_with_acquisition_v2 NOT OCLC_every_physical_title_except_acquisition_v2

class CreateSet:
    def run(self) :
        # Sandbox
        secrets = dotenv_values(".env")
        api_key = secrets["API_KEY"]
        set_operator = 'NOT'

        # Small sets to test with:
        # set1 = '36047088550006381'
        # set2 = '36047088600006381'

        # Small sets to test with (these should work in both Sandbox and Production):
        # set1 = '28272064010006381' # Dmf one record
        # set2 = '20623624350006381' # dmf one record 2022-01-27
        # These small sets to test with are just in the Sandbox and are Physical Titles sets:
        # set1 = '36137129480006381' # Dmf one record new
        # set2 = '36137129530006381' # Dmf one more record

        # # The real sets:
        set1 = '34493393360006381'
        set2 = '22766924310006381'

        payload = '''
        {
          "status" : {
              "desc" : "Active",
              "value" : "ACTIVE"
          },
          "description" : null,
          "origin" : {
              "desc" : "Institution only",
              "value" : "UI"
          },
          "note" : null,
          "query" : null,
          "members" : null,
          "link" : "",
          "private" : {
              "desc" : "No",
              "value" : "false"
          },
          "type" : {
              "desc" : "Itemized",
              "value" : "ITEMIZED"
          },
          "content" : {
              "value" : "IEP"
          },
          "created_by" : {
            "desc" : "API, Ex Libris",
            "value" : "exl_api"
          }
        }
        '''

        # Create a request
        headers = {'Authorization': f'apikey {api_key}', 'content_type': 'application/json', 'Accept': 'application/json'}
        create_url = f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets?combine={set_operator}&set1={set1}&set2={set2}"
        payload_as_json = json.loads(payload)

        # Send the request
        r = requests.post(create_url, headers=headers, json=payload_as_json)

        # Check the results of the request

        # Status code
        # print(r.status_code)

        # The full response
        # print(r.text)

        # The JSON response, if any
        # pretty_json = json.dumps(r.json(), indent=4)
        # print(pretty_json)

        # Status code 200 means success, Status Code 503 means <errorCode>ROUTING_ERROR</errorCode> which is a timeout which means success.
        if r.status_code == 200 or r.status_code == 503:
            print("Created the set.")
        else:
            print("There was a problem.")

if __name__ == "__main__":
    #print("name is main")
    #a = CreateSet()
    #a.run()
    CreateSet().run()
