def check_response(response_raw):
    if response_raw.status_code in (200, 201, 202):
        response = response_raw.json()
        return response['data']
    else:
        print(response_raw.content.decode())
        raise response_raw.raise_for_status()