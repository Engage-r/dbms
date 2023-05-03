import streamlit as st
import pandas as pd


# define function to book tickets
def book_ticket(source, destination, date, num_seats, ticket_class):
    # do some processing here to book the ticket
    # this is just a dummy implementation for demonstration purposes
    st.write(
        f"Booking {num_seats} {ticket_class} tickets from {source} to {destination} on {date}"
    )
    st.write("Ticket booked successfully!")


# define the book ticket page
def book_ticket_page():
    st.header("Book Ticket")

    # get user input for booking ticket
    source = st.text_input("Enter source station ID:")
    destination = st.text_input("Enter destination station ID:")
    date = st.date_input("Enter travel date:")
    num_seats = st.number_input(
        "Enter number of seats:", min_value=1, max_value=10, step=1
    )
    # ticket_class = st.selectbox(
    #     "Select ticket class:", ("1AC", "2AC", "3AC", "SL", "2S")
    # )

    # show available trains for selected source, destination, and date
    # st.write("Available Trains:")
    # trains_df = pd.read_csv("trains.csv") # assuming the train data is stored in a CSV file
    # available_trains = trains_df[(trains_df["Source"]==source) & (trains_df["Destination"]==destination) & (trains_df["Date"]==date)]
    # st.dataframe(available_trains)

    # book the ticket
    if st.button("Book Ticket"):
        book_ticket(source, destination, date, num_seats)


# run the app
if __name__ == "__main__":
    book_ticket_page()
