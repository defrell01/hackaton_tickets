from pydantic import BaseModel


class ApiRequest(BaseModel):
    departure_city: str
    destination_city: str
    date: str
    numberOfAdults: int
    cabinClass: str


class PredictData(BaseModel):
    source_city: str
    departure_time: str
    stop: str
    arrival_time: str
    destination_city: str
    class_flight: str
    duration: float
    days_left: int


class RoundTripRequest(BaseModel):
    departure_city: str
    destination_city: str
    departure_date: str
    back_departure_date: str
    numberOfAdults: int
    cabinClass: str
