import functions_framework
import json, time, requests, os
from google.cloud import storage

@functions_framework.http
def hello_http(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    print('Stating Execution')
    
    API_KEY = os.environ.get("API_KEY")
    API_URL = f"https://api.the-odds-api.com/v4/sports/americanfootball_nfl/odds/?regions=us&oddsFormat=american&markets=h2h,spreads,totals&apiKey={API_KEY}"
    BUCKET = "dione"
    
    ts = time.time()
    call_api_and_upload_json_to_gcs(API_URL, BUCKET, f"data/{ts}-odds-api.json")
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'name' in request_json:
        name = request_json['name']
    elif request_args and 'name' in request_args:
        name = request_args['name']
    else:
        name = 'World'
    return 'Hello {}!'.format(name)



def call_api_and_upload_json_to_gcs(api_url, cloud_storage_bucket_name, cloud_storage_object_name):
  """Calls the specified API and uploads the resulting JSON to a Cloud Storage bucket.

  Args:
    api_url: The URL of the API to call.
    cloud_storage_bucket_name: The name of the Cloud Storage bucket to upload the JSON response to.
    cloud_storage_object_name: The name of the object in the Cloud Storage bucket to save the JSON response to.

  Returns:
    None.
  """

  response = requests.get(api_url)

  if response.status_code == 200:

    json_data = response.json()

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(cloud_storage_bucket_name)
    blob = bucket.blob(cloud_storage_object_name)
    blob.upload_from_string(json.dumps(json_data), content_type='application/json')

    print('JSON data saved to Cloud Storage bucket successfully.')
  else:
    print('Error making API call:', response.status_code, response.content)




