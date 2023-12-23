import streamlit as st
import pandas as pd
import codecs
import json
from datetime import date, timedelta, datetime
from reqs import *


st.set_page_config(page_title="Поиск авиабилетов", page_icon=":airplane:", layout="wide")


username = st.sidebar.text_input("Логин")
password = st.sidebar.text_input("Пароль", type="password")
if st.sidebar.button("Войти"):
    if username == "admin" and password == "12345":
        st.success("Успешная аутентификация")
    else:
        st.error("Неправильный логин или пароль")


def load_css(file_name:str)->None:
    with open('styles.css', 'r', encoding='utf-8') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def extract_hours_minutes(dt_string):
    dt_obj = pd.to_datetime(dt_string)
    return dt_obj.strftime('%H:%M')

def convert_duration(duration_str):
    parts = duration_str.split()
    if len(parts) == 2:
        hours, minutes = parts
        hours = hours.replace('h', 'ч')
        minutes = minutes.replace('m', 'мин')
        return f"{hours} {minutes}"
    elif len(parts) == 1 and 'h' in duration_str:
        hours = duration_str.replace('h', 'ч')
        return f"{hours} 0мин"
    else:
        # Обработка неожиданного формата
        return duration_str  

def days_until_departure(departure_date):
    departure_datetime = datetime.strptime(departure_date, '%Y-%m-%d') 
    today_datetime = datetime.now()  
    days_until = (departure_datetime - today_datetime).days 
    return days_until


load_css("styles.css")

with open("header.html", 'r', encoding='utf-8') as f:
    header_html = f.read()

st.markdown(header_html, unsafe_allow_html=True)



with st.form(key='flight_search_form'):

    col1, col2 = st.columns([1, 1])

    departure = col1.text_input("",placeholder="Откуда")
    arrival = col2.text_input("",placeholder="Куда")

    col3, col4, col5, col6 = st.columns([1, 1, 1, 1])

    departure_date = col3.date_input("Дата вылета:", date.today())
    returnFlight_date = col4.date_input("Дата обратного вылета:", date.today() + timedelta(days=1))
    class_type = col5.selectbox("Класс:", ("Эконом", "Бизнес", "Первый"))
    passengers = col6.number_input("Количество пассажиров:", min_value=1, max_value=100, value=1)

    if class_type == 'Эконом':
        class_type = 'Economy'
    elif class_type == 'Бизнес':
        class_type = 'Business'
    elif class_type == 'Первый':
        class_type = 'Business'

    departure_date = departure_date.strftime("%Y-%m-%d")
    returnFlight_date = returnFlight_date.strftime("%Y-%m-%d")

    search_button = st.form_submit_button(label="Найти билеты 🔍")


if search_button:

    try:

        round_flight_request(departure, arrival, departure_date, returnFlight_date, passengers, class_type)

        with open('round.json', 'r', encoding='utf-8') as f:
            saved_user_data = json.load(f)

        df = pd.DataFrame(saved_user_data)

        df['departure_time'] = df['departure_time'].apply(extract_hours_minutes)
        df['arrival_time'] = df['arrival_time'].apply(extract_hours_minutes)
        df['duration'] = df['duration'].apply(convert_duration)

        forth_flights = df[df['flight_type'] == 'forth'].copy()
        back_flights = df[df['flight_type'] == 'back'].copy()

        forth_flights = forth_flights[forth_flights['flight_type'] == 'forth'].copy().reset_index(drop=True)
        back_flights = back_flights[back_flights['flight_type'] == 'back'].copy().reset_index(drop=True)

        back_flights = back_flights.drop('flight_type', axis=1)
        forth_flights = forth_flights.drop('flight_type', axis=1)
        
        back_flights = back_flights.rename(columns={
            "airline_code": 'Код авиакомпании',
            "flight": 'Рейс',
            "departure_city": 'Город отправления',
            "departure_time": 'Время отправления',
            "stops": 'Пересадки',
            "arrival_time": 'Время прибытия',
            "arrival_cty": 'Город прибытия',
            "cabin_class": 'Класс',
            "duration": 'Длительность',
            "days_left": 'Дней до вылета',
            "price": 'Цена, руб'
        })

        forth_flights = forth_flights.rename(columns={
            "airline_code": 'Код авиакомпании',
            "flight": 'Рейс',
            "departure_city": 'Город отправления',
            "departure_time": 'Время отправления',
            "stops": 'Пересадки',
            "arrival_time": 'Время прибытия',
            "arrival_cty": 'Город прибытия',
            "cabin_class": 'Класс',
            "duration": 'Длительность',
            "days_left": 'Дней до вылета',
            "price": 'Цена, руб'
        })

        st.markdown("**Туда**")
        st.write(forth_flights)
        
        st.markdown("**Обратно**")
        st.write(back_flights)

        back_min_price_row = back_flights.loc[back_flights['Цена, руб'].idxmin()]
        forth_min_price_row = forth_flights.loc[forth_flights['Цена, руб'].idxmin()]
        total_price = forth_min_price_row['Цена, руб'] + back_min_price_row['Цена, руб']

        html_content1 = """
        <div class="resultPlus">
            <div class="result">
                <div class="cost">
                    <h2>{}</h2>
                    <p>, руб.</p>
                </div>
                <div class="info">
                    <p></p>
                    <p>{}</p>
                    <p></p>
                    <p></p>
                    <p></p>
                    <p>{}</p>
                </div>
            </div>
        </div>
        """.format(total_price,
                forth_min_price_row['Рейс'],
                back_min_price_row['Рейс']
                )

        st.markdown("Самый выгодный вариант")
        st.markdown(html_content1, unsafe_allow_html=True)

    except requests.HTTPError as err:
        if err.response.status_code == 400:
            predict_price(departure, '', '', '', arrival, class_type, 0, days_until_departure(departure_date))

            with open('predict.json', 'r', encoding='utf-8') as f:
                first_predicted_data = json.load(f)

            first_price = int(first_predicted_data['price'])

            print(first_price)

            # with open('round.json', 'r', encoding='utf-8') as f:
            #     saved_user_data1 = json.load(f)

            # df1 = pd.DataFrame(saved_user_data1)

            predict_price(arrival, '', '', '', departure, class_type, 0, days_until_departure(returnFlight_date))

            with open('predict.json', 'r', encoding='utf-8') as f:
                second_predicted_data = json.load(f)

            second_price = int(first_predicted_data['price'])

            print(second_price)
            
            # df2 = pd.DataFrame(saved_user_data2)

            total_price = first_price + second_price
            
            html_content1 = """
            <div class="resultPlus">
                <div class="result">
                    <div class="cost">
                        <h2>{}</h2>
                        <p>, руб.</p>
                    </div>
                    <div class="info">
                        <p>Дней до вылета {}</p>
                        <p>{} - {}</p>
                        <p>{}</p>
                    </div>
                </div>
            </div>
            """.format(total_price,
                       days_until_departure(departure_date),
                       departure, 
                       arrival,
                       class_type,
                      )

            st.markdown("**Прогноз стоимости**")
            st.markdown(html_content1, unsafe_allow_html=True)
    