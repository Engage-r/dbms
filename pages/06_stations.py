import streamlit as st
import pandas as pd
import psycopg2

# define the available stations page
def available_stations_page():
    st.header("Available Stations")

    # read station data from CSV file
    conn = psycopg2.connect(
        host="localhost",
        database="t2",
        user="postgres",
        password="password"
    )

    # create a cursor object to execute SQL queries
    cur = conn.cursor()

    # execute the SQL query to retrieve all stations
    cur.execute("SELECT * FROM railway_station")

    # fetch all rows and convert the result to a pandas dataframe
    stations_df = pd.DataFrame(cur.fetchall(), columns=["Station Code", "Station Name"])

    # show the dataframe in Streamlit
    st.write("All Stations:")
    st.dataframe(stations_df)

    # close the cursor and database connection
    cur.close()
    conn.close()
# run the app
if __name__ == "__main__":
    available_stations_page()
