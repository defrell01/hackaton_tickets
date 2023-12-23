import requests
import json


def round_flight_request(departure_city, destination_city, departure_date, back_departure_date, number_of_adults, cabin_class):
    url = 'http://127.0.0.1:8000/getRoundFlight/'
    headers = {'Content-Type': 'application/json'}

    print(departure_city)
    data = {
        "departure_city": departure_city,
        "destination_city": destination_city,
        "departure_date": departure_date,
        "back_departure_date": back_departure_date,
        "numberOfAdults": number_of_adults,
        "cabinClass": cabin_class
    }

    print(data)

    try:
        response = requests.get(url, json=data, headers=headers)
        response.raise_for_status()

        with open("round.json", "w") as json_file:
            json.dump(response.json(), json_file, indent=4)

    except Exception as e:
        raise e
    

def predict_price(source_city, departure_time, stop, arrival_time, destination_city, class_flight, duration, days_left):
    url = 'http://127.0.0.1:8000/predictPrice/'
    headers = {'Content-Type': 'application/json'}

    data = {
        "source_city": source_city,
        "departure_time": departure_time,
        "stop": stop,
        "arrival_time": arrival_time,
        "destination_city": destination_city,
        "class_flight": class_flight,
        "duration": duration,
        "days_left": days_left
    }

    print(data)

    try:
        response = requests.get(url, json=data, headers=headers)
        response.raise_for_status()

        with open("predict.json", "w") as json_file:
            json.dump(response.json(), json_file, indent=4)

    except Exception as e:
        raise e
    