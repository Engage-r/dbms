import streamlit as st
import pandas as pd
import psycopg2

# define the available trains page
def available_trains_page():
    st.header("Available Trains")

    # get user input for source, destination, and date
    source = st.text_input("Enter source station:")
    destination = st.text_input("Enter destination station:")
    date = st.date_input("Enter travel date:")

    # show available trains for selected source, destination, and date
    st.write("Available Trains:")
    conn = psycopg2.connect(
            host="localhost",
            database="t2",
            user="postgres",
            password="password"
    )

    # create a cursor object to execute SQL queries
    cur = conn.cursor()

    if st.button("Search"):
        # execute the find_trains_btw_stations function to get available trains
        cur.execute("SELECT * FROM find_trains_btw_stations(%s, %s, %s)", (source, destination, date))
        available_trains = cur.fetchall()

        # convert the result to a pandas dataframe and show it in Streamlit
        print(available_trains)
        print("--------------------------------")
        trains_df = pd.DataFrame(available_trains, columns=["Train Number", "Train Name", "Source", "Destination"])
        st.dataframe(trains_df)


    # close the cursor and database connection
    cur.close()
    conn.close()

# run the app
if __name__ == "__main__":
    available_trains_page()
