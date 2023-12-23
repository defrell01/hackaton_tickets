import requests
import os
from db.models import ApiRequest, RoundTripRequest


def load_env_variables(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value


def get_flight(ApiRequest):
    try:

        load_env_variables('.env')
        api_key = os.environ.get('API_KEY')

        code_dest = requests.get(
            f'https://api.flightapi.io/iata/{api_key}?name={ApiRequest.destination_city}&type=airport')

        code_dep = requests.get(
            f'https://api.flightapi.io/iata/{api_key}?name={ApiRequest.departure_city}&type=airport')

        resp = requests.get(f'https://api.flightapi.io/onewaytrip/{api_key}/{code_dest.json()['data'][0]['iata']}/'
                            f'{code_dep.json()['data'][0]['iata']}/{ApiRequest.date}/{ApiRequest.numberOfAdults}/0/0/'
                            f'{ApiRequest.cabinClass}'
                            f'/USD')
        return resp

    except Exception as e:
        raise e


def get_round_flight(RoundTripRequest):
    try:

        data = []

        load_env_variables('.env')
        api_key = os.environ.get('API_KEY')

        code_dest = requests.get(
            f'https://api.flightapi.io/iata/{api_key}?name={RoundTripRequest.destination_city}&type=airport')

        code_dep = requests.get(
            f'https://api.flightapi.io/iata/{api_key}?name={RoundTripRequest.departure_city}&type=airport')

        resp = requests.get(f'https://api.flightapi.io/onewaytrip/{api_key}/{code_dest.json()['data'][0]['iata']}/'
                            f'{code_dep.json()['data'][0]['iata']}/{RoundTripRequest.departure_date}/{RoundTripRequest.numberOfAdults}/0/0/'
                            f'{RoundTripRequest.cabinClass}'
                            f'/USD')

        back_resp = requests.get(f'https://api.flightapi.io/onewaytrip/{api_key}/{code_dep.json()['data'][0]['iata']}/'
                                 f'{code_dest.json()['data'][0]['iata']}/{RoundTripRequest.back_departure_date}/{RoundTripRequest.numberOfAdults}/0/0/'
                                 f'{RoundTripRequest.cabinClass}'
                                 f'/USD')

        data.append(resp)
        data.append(back_resp)

        return data

    except Exception as e:
        print(e)
        raise e
