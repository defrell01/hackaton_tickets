import sqlite3


def add_flight(data):
    conn = sqlite3.connect('../sfhack.sqlite')
    cursor = conn.cursor()

    try:
        cursor.execute('''
                    INSERT INTO main.Flights(airline, flight, source_city, departure_time, stops, arrival_time,
                    destination_city, class, duration, days_left, price, data_source)
                    VALUES (?, ?, ?, ?, ?, ?,
                    ?, ?, ?, ?, ?, ?)
                ''', (data[0], data[1], data[2], data[3], data[4], data[5],
                      data[6], data[7], data[8], data[9], data[10], "API"))
    except sqlite3.Error as e:
        print(e)
    finally:
        conn.close()
