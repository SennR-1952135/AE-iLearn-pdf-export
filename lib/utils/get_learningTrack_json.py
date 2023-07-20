
import requests

def get_learningTrack_json(api_url, bearer_token):    
    print("processing url: ", api_url)

    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to get learning track json (status code: " + str(response.status_code) + ")" )

    return response.json()