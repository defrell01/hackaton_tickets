from util import parse_json_flights, parse_json_round_flights
from fastapi import FastAPI, HTTPException
import uvicorn
from db.models import ApiRequest, PredictData, RoundTripRequest
from db.database import add_flight
from req.getFlight import get_flight, get_round_flight
from model.predict import predict_price

app = FastAPI()


@app.get("/getFlight")
def get_flight_endpoint(flight: ApiRequest):
    try:
        res = get_flight(flight)

        data = parse_json_flights(res, len(res.json()))

        add_flight(data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        return data


@app.get("/getFlight/")
def get_flight_round_endpoint(flight: ApiRequest):
    try:
        res = get_flight(flight)

        data = parse_json_flights(res, len(res.json()))

        add_flight(data)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        return data


@app.get("/predictPrice")
def predict_price_endpoint(entry: PredictData):
    try:
        data = predict_price(entry)

        print(data)

        return {"airline_code": "unknown",
                "flight": "unknown",
                "departure_city": entry.source_city,
                "departure_time": entry.departure_time,
                "stops": entry.stop,
                "arrival_time": "unknown",
                "arrival_cty": entry.destination_city,
                "cabin_class": entry.class_flight,
                "duration": entry.duration,
                "days_left": entry.days_left,
                "price": data[0]
                }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/getRoundFlight")
def get_round_flight_endpoint(RoundTripRequest: RoundTripRequest):
    try:
        res = get_round_flight(RoundTripRequest)
        data = parse_json_round_flights(res, len(res))

        return data

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)