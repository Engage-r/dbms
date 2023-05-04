import streamlit as st
import psycopg2
import pandas as pd

def show_train_route():
    # Define the train route for each train number

    # Get the train number from the user
    train_number = st.text_input("Enter train number:")

    if st.button("Show Train Route"):
        conn = psycopg2.connect(
        host="localhost",
        database="t2",
        user="postgres",
        password="password"
    )


        # create a cursor object to execute SQL queries
        cur = conn.cursor()

        
        cur.execute("SELECT * FROM train_stations where train_no=%s", (int(train_number),))
        # train_routes = cur.fetchall()

        train_routes = pd.DataFrame(cur.fetchall(), columns=["Train no", "Station Name"])

                # Split the station names using str.split() method
        train_routes["Stations"] = train_routes["Station Name"].str.split(",")

        # Use explode() to create a new row for each station
        train_routes = train_routes.explode("Stations")

        # Drop unnecessary columns
        train_routes.drop(columns=["Train no", "Station Name"], inplace=True)
        print(train_routes)
        # Show the train route if the user has entered a valid train number
        if not train_routes.empty:
            st.table(train_routes)

        # Show the train route if the user has entered a valid train number


# Create a page to show the train route
st.title("Train Route")
show_train_route()
