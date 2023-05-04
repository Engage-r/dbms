import streamlit as st
import pandas as pd
import psycopg2

# define the booked tickets page
def booked_tickets_page(user_email):
    st.header("Booked Tickets")

    # load the ticket data from the CSV file
    user_id = st.session_state["user"]

    conn = psycopg2.connect(
        host="localhost",
        database="t2",
        user="postgres",
        password="password"
    )

    # create a cursor object to execute SQL queries
    cur = conn.cursor()

    # execute the SQL query to retrieve all stations
    cur.execute("SELECT * FROM ticket WHERE user_id = %s", (int(user_id),))

    user_tickets_df = pd.DataFrame(cur.fetchall(), columns=["PNR", "Src Station Name", "Dest Station Name", "Train No", "User_id", "Date", "No of seats"])

# add a "Cancel" button column to the dataframe using the apply method

    # display the ticket data in a table
    if len(user_tickets_df) > 0:
        st.write(user_tickets_df[["PNR", "Src Station Name", "Dest Station Name", "Train No","Date", "No of seats"]])
    else:
        st.write("You have not booked any tickets yet.")

# run the app
if __name__ == "__main__":
    user_email = "example@example.com" # replace with the user's email address
    booked_tickets_page(user_email)
