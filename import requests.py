import requests
import time

FITBIT_BASE_URL = "https://api.fitbit.com/1/user/-/"
HEART_RATE_ENDPOINT = "activities/heart/date/today/1d/1sec/time/00:00/23:59.json"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1I4TFoiLCJzdWIiOiJCUUM5OVoiLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJyc29jIHJzZXQgcm94eSBybnV0IHJwcm8gcnNsZSByYWN0IHJyZXMgcmxvYyByd2VpIHJociBydGVtIiwiZXhwIjoxNjk1NzA5Mjg0LCJpYXQiOjE2OTU2ODA0ODR9.fVNpiV4f7FJhOMLGvU8_E8bRMyAqsOl-F9yd7B3zH7w"  # Your token here
HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
}
THRESHOLD = 60  # Set the threshold to 60 BPM

def get_current_heart_rate():
    response = requests.get(FITBIT_BASE_URL + HEART_RATE_ENDPOINT, headers=HEADERS)
    data = response.json()

    # Log the response status and data for debugging
    print(f"Response Status: {response.status_code}")
    print(f"Response Data: {data}")

    # Ensure the response contains heart rate data
    if 'activities-heart-intraday' in data and 'dataset' in data['activities-heart-intraday']:
        last_data_point = data['activities-heart-intraday']['dataset'][-1]
        return last_data_point['value']
    else:
        return None

while True:
    heart_rate = get_current_heart_rate()
    if heart_rate is None:
        print("Unable to fetch heart rate data.")
    else:
        print(f"Current Heart Rate: {heart_rate} BPM")
        if heart_rate < THRESHOLD:
            print("Heart rate below threshold. Exiting...")
            break

    time.sleep(5)  # Sleep for 5 seconds before the next call