import streamlit as st
import pandas as pd

# define the booked tickets page
def booked_tickets_page(user_email):
    st.header("Booked Tickets")

    # load the ticket data from the CSV file
    tickets_df = pd.read_csv("tickets.csv")

    # filter the ticket data by the user's email address
    user_tickets_df = tickets_df[tickets_df["Email"]==user_email]

    # display the ticket data in a table
    if len(user_tickets_df) > 0:
        st.write(user_tickets_df[["Ticket ID", "Source", "Destination", "Date", "Seats"]])
    else:
        st.write("You have not booked any tickets yet.")

# run the app
if __name__ == "__main__":
    user_email = "example@example.com" # replace with the user's email address
    booked_tickets_page(user_email)
