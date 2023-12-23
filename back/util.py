from datetime import datetime


def parse_json_flights(data, amount):
    data = data.json()
    legs = data['legs']
    fares = data['fares']
    flight_data = []

    for i in range(amount):
        price = fares[i]['price']['amount']
        airline_code = legs[i]['airlineCodes'][0]
        flight = legs[i]['segments'][0]['designatorCode']
        arrival_city = legs[i]['arrivalAirportCode']
        dep_city = legs[i]['departureAirportCode']
        stops = legs[i]['stopoversCount']
        departure_time = legs[i]['departureDateTime']
        arrival_time = legs[i]['arrivalDateTime']
        target_date = datetime.fromisoformat(departure_time[0:19])
        current_date = datetime.now()
        difference = target_date - current_date
        days_left = difference.days

        cabin_class = legs[i]['segments'][0]['cabin']
        duration = legs[i]['duration']

        flight_dict = {
            "airline_code": airline_code,
            "flight": flight,
            "departure_city": dep_city,
            "departure_time": departure_time,
            "stops": stops,
            "arrival_time": arrival_time,
            "arrival_cty": arrival_city,
            "cabin_class": cabin_class,
            "duration": duration,
            "days_left": days_left,
            "price": 91 * price
        }

        flight_data.append(flight_dict)

    return flight_data


def parse_json_round_flights(data, amount):
    flight_data = []

    for idx, response in enumerate(data):
        flight_info = response.json()
        legs = flight_info['legs']
        fares = flight_info['fares']

        for i in range(amount):
            price = fares[i]['price']['amount']
            airline_code = legs[i]['airlineCodes'][0]
            flight = legs[i]['segments'][0]['designatorCode']
            arrival_city = legs[i]['arrivalAirportCode']
            dep_city = legs[i]['departureAirportCode']
            stops = legs[i]['stopoversCount']
            departure_time = legs[i]['departureDateTime']
            arrival_time = legs[i]['arrivalDateTime']
            target_date = datetime.fromisoformat(departure_time[0:19])
            current_date = datetime.now()
            difference = target_date - current_date
            days_left = difference.days

            cabin_class = legs[i]['segments'][0]['cabin']
            duration = legs[i]['duration']

            flight_dict = {
                "airline_code": airline_code,
                "flight": flight,
                "departure_city": dep_city,
                "departure_time": departure_time,
                "stops": stops,
                "arrival_time": arrival_time,
                "arrival_cty": arrival_city,
                "cabin_class": cabin_class,
                "duration": duration,
                "days_left": days_left,
                "price": 91 * price,
                "flight_type": "forth" if idx % 2 == 0 else "back"
            }

            flight_data.append(flight_dict)

    return flight_data
