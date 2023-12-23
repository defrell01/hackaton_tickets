import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle
import joblib
from db.models import PredictData


def predict_price(input_data: PredictData):

    loaded_model = joblib.load("model/RF_model.pkl")
    full_pipeline = joblib.load("model/full_pipeline.pkl")

    df = pd.DataFrame([[input_data.source_city,
                        input_data.departure_time, input_data.stop,
                        input_data.arrival_time, input_data.destination_city,
                        input_data.class_flight, input_data.duration, input_data.days_left]],
                      columns=["source_city", "departure_time", "stops", "arrival_time",
                               "destination_city", "class", "duration", "days_left"])
    df.index.name = 'id'
    df = pd.DataFrame(df)
    df.to_csv('file.csv')

    data = pd.read_csv('file.csv', index_col='id')

    le = LabelEncoder()
    data['source_city'] = le.fit_transform(data['source_city'])
    data['destination_city'] = le.fit_transform(data['destination_city'])
    data['class'] = le.fit_transform(data['class'])
    data['stops'] = le.fit_transform(data['stops'])
    data['class'] = le.fit_transform(data['class'])
    data['departure_time'] = le.fit_transform(data['departure_time'])
    data['arrival_time'] = le.fit_transform(data['arrival_time'])

    prep = full_pipeline.transform(data)
    predict = loaded_model.predict(prep)

    return predict
