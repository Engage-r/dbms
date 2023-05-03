import streamlit as st
import pandas as pd

# define the available stations page
def available_stations_page():
    st.header("Available Stations")

    # read station data from CSV file
    stations_df = pd.read_csv("stations.csv") # assuming the station data is stored in a CSV file

    # show the available stations in a table
    st.write("All Stations:")
    st.dataframe(stations_df[["Station Code", "Station Name"]])

# run the app
if __name__ == "__main__":
    available_stations_page()
