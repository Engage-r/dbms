import streamlit as st
import pandas as pd
import psycopg2

psycopg2.extras.register_uuid()
import uuid

# define the cancel ticket page
def cancel_ticket_page():
    st.header("Cancel Ticket")

    # get user input for ticket ID
    pnr = st.text_input("Enter ticket ID:")
    conn = psycopg2.connect(
        host="localhost",
        database="t2",
        user="postgres",
        password="password"
    )

    # create a cursor object to execute SQL queries
    cur = conn.cursor()

    if st.button("Cancel Ticket"):
        pnr = uuid.UUID(pnr)

        # execute the SQL query to retrieve all stations
        cur.execute("SELECT * FROM ticket where pnr=%s", (pnr,))
        row = cur.fetchone()
        print(row)
        print("++++++++++++++++++===")
        # check if the ticket ID is valid and cancel the ticket
        
        if row:
            cur.execute("DELETE FROM  ticket WHERE pnr = %s", (pnr,))
            conn.commit()
            st.success("Ticket successfully cancelled!")
        else:
            st.error("Invalid ticket ID. Please try again.")

# run the app
if __name__ == "__main__":
    cancel_ticket_page()
