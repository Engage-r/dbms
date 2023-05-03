import streamlit as st
import pandas as pd
import random

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


def show_available_seats(source, destination, date):
    # Filter the available trains based on the source and destination
    available_trains_filtered = [
        train
        for train in available_trains
        if train["source"] == source and train["destination"] == destination
    ]

    # Show the available trains and their seat counts
    if len(available_trains_filtered) > 0:
        st.write(f"Available seats from {source} to {destination} on {date}:")
        rows = []
        for train in available_trains_filtered:
            row = [train["train_number"], train["name"]]
            for seat_type, seat_count in train["seats"].items():
                row.append(seat_count)
            rows.append(row)
        st.write(
            pd.DataFrame(
                rows, columns=["Train Number", "Name", "1AC", "2AC", "3AC", "SL", "2S"]
            )
        )
    else:
        st.write(f"No trains available from {source} to {destination} on {date}.")


# Create a page to show the available seats
st.title("View Available Seats")
source = st.text_input("Enter the source station:")
destination = st.text_input("Enter the destination station:")
date = st.date_input("Enter the travel date:")
if st.button("Search"):
    show_available_seats(source, destination, date.strftime("%d-%m-%Y"))
