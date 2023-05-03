import streamlit as st
import pandas as pd

# define the available trains page
def available_trains_page():
    st.header("Available Trains")

    # get user input for source, destination, and date
    source = st.text_input("Enter source station:")
    destination = st.text_input("Enter destination station:")
    date = st.date_input("Enter travel date:")

    # show available trains for selected source, destination, and date
    st.write("Available Trains:")
    trains_df = pd.read_csv("trains.csv") # assuming the train data is stored in a CSV file
    available_trains = trains_df[(trains_df["Source"]==source) & (trains_df["Destination"]==destination) & (trains_df["Date"]==date)]
    st.dataframe(available_trains)

# run the app
if __name__ == "__main__":
    available_trains_page()
