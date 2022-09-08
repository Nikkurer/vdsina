import requests


def check_response(response_raw):
    if response_raw.status_code == requests.codes.ok:
        response = response_raw.json()
        return response['data']
    else:
        print(response_raw.content.decode())
        exit(1)