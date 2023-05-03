import streamlit as st
import pandas as pd

# define the cancel ticket page
def cancel_ticket_page():
    st.header("Cancel Ticket")

    # get user input for ticket ID
    ticket_id = st.text_input("Enter ticket ID:")

    # check if the ticket ID is valid and cancel the ticket
    tickets_df = pd.read_csv("tickets.csv") # assuming the ticket data is stored in a CSV file
    if ticket_id in tickets_df["Ticket ID"].values:
        tickets_df = tickets_df[tickets_df["Ticket ID"]!=ticket_id]
        tickets_df.to_csv("tickets.csv", index=False) # update the ticket data CSV file
        st.success("Ticket successfully cancelled!")
    elif ticket_id != "":
        st.error("Invalid ticket ID. Please try again.")

# run the app
if __name__ == "__main__":
    cancel_ticket_page()
