import requests
import json
from datetime import date
from dotenv import dotenv_values

# This program runs the “Set Management Tags” job on the newly created itemized set 
# and it sets the Management Tags of all members of that set to "Don’t publish" regardless of what it has for a Management Tag.
# The first part retrieves the set metadata from Alma, the second part submits the job to Alma.

class ChangeTags:
    def run(self) :
        today = date.today()
        year = today.year
        month = f"{today.month:02d}"
        day = f"{today.day:02d}"

        # First get the Set ID and Name of the Set to run the job with...
        # This is the new set name pattern
        unaddset_name_pattern = f"OCLC_every_physical_title_with_acquisition_v2 - Combined - {month}/{day}/{year}"
        # This is the little set name pattern
        # unaddset_name_pattern = f"Dmf one record new - Combined - {month}/{day}/{year}"

        secrets = dotenv_values(".env")
        api_key = secrets["API_KEY"]

        # Create a request
        headers = {'Authorization': f'apikey {api_key}', 'content_type': 'application/json', 'Accept': 'application/json'}
        url_base = f"https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/sets?set_type=ITEMIZED&q=name~{unaddset_name_pattern}&limit=1&offset=0"

        # Send the request
        r = requests.get(url_base, headers=headers)

        # Handle the response
        try:
            # pretty_json = json.dumps(r.json(), indent=4)
            # print(pretty_json)
            unaddset_id = r.json()["set"][0]["id"]
            # print(unaddset_id)
            unaddset_name = r.json()["set"][0]["name"]
            # print(unaddset_name)
        except:
            print("There was a problem.")

        print("Starting the Set Mgmt Tags job...")

        flag_action = "NONE"
        job_name = 'Synchronize Bib records with OCLC - do not publish'
        set_id = unaddset_id
        set_name = unaddset_name

        #
        # Payload
        #
        job_info = f'''
        {{
          "parameter" : [
            {{
                "name" : {{ "value" : "task_MmsTaggingParams_boolean"}},
                "value" : "{flag_action}"
            }},
            {{
                "name" : {{ "value" : "set_id" }},
                "value" : "{set_id}"
            }},
            {{
                "name" : {{ "value" : "job_name" }},
                "value" : "{job_name} - {set_name}"
            }}
          ]
        }}
        '''
        payload_as_json = json.loads(job_info)

        # Create a request
        headers = {'Authorization': f'apikey {api_key}', 'content_type': 'application/json', 'Accept': 'application/json'}
        set_mgt_tags_url = "https://api-na.hosted.exlibrisgroup.com/almaws/v1/conf/jobs/M12889770000231?op=run"

        # Send the request
        r = requests.post(set_mgt_tags_url, headers=headers, json=payload_as_json)

        # Check the results of the request
        # Status code
        # print(r.status_code)

        # The full response
        # print(r.text)

        # The JSON response, if any
        # pretty_json = json.dumps(r.json(), indent=4)
        # print(pretty_json)

        # Status code 200 means success.
        if r.status_code == 200:
            print("Set Mgmt Tags job submitted.")
        else:
            print("Something went wrong.")

if __name__ == "__main__":
    # print("name is main")
    # a = ChangeTags()
    # a.run()
    ChangeTags().run()