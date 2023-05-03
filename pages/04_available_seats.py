import streamlit as st
import pandas as pd
import random
import psycopg2

# Define the available trains and their seat counts
available_trains = [
    {
        "train_number": "12345",
        "name": "Express",
        "source": "Station A",
        "destination": "Station B",
        "seats": {"1AC": 10, "2AC": 20, "3AC": 30, "SL": 100, "2S": 200},
    },
    {
        "train_number": "67890",
        "name": "Superfast",
        "source": "Station X",
        "destination": "Station Y",
        "seats": {"1AC": 5, "2AC": 10, "3AC": 20, "SL": 50, "2S": 100},
    },
    {
        "train_number": "24680",
        "name": "Local",
        "source": "Station P",
        "destination": "Station Q",
        "seats": {"1AC": 0, "2AC": 5, "3AC": 10, "SL": 20, "2S": 50},
    },
]


def show_available_seats(train_number, source, destination, date, num_seats):
    # Filter the available trains based on the source and destination
    
    conn = psycopg2.connect(
            host="localhost",
            database="t2",
            user="postgres",
            password="password"
    )

    # create a cursor object to execute SQL queries
    cur = conn.cursor()

        # execute the find_trains_btw_stations function to get available trains

    cur.execute("SELECT * FROM get_min_avail_seats(%s, %s, %s, %s)", (int(train_number), int(source), int(destination), date))
    available_trains = cur.fetchone()
    # row = cur.fetchone()


    # convert the result to a pandas dataframe and show it in Streamlit
    # print(row)
    print(available_trains)
    print("--------------------------------")



    # close the cursor and database connection
    cur.close()
    conn.close()
    

    # Show the available trains and their seat counts
    if available_trains[0] > 0:
        st.write(f"Available seats from {source} to {destination} on {date}: {available_trains[0]}")
    else:
        st.write(f"No trains available from {source} to {destination} on {date}.")


# Create a page to show the available seats
st.title("View Available Seats")
train_number = st.text_input("Enter the train number:")
source = st.text_input("Enter the source station:")
destination = st.text_input("Enter the destination station:")
date = st.date_input("Enter the travel date:")
num_seats = st.number_input("Enter the number of seats:", min_value=1, step=1)
if st.button("Search"):
    show_available_seats(train_number, source, destination, date, num_seats)
