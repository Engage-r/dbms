import streamlit as st
import pandas as pd

# create a dictionary of available trains and their seat availability
available_trains = {
    "Train A": {"1A": 2, "2A": 5, "Sleeper": 10},
    "Train B": {"1A": 1, "2A": 3, "Sleeper": 8},
    "Train C": {"1A": 3, "2A": 2, "Sleeper": 12},
}

# create a dataframe to store ticket bookings
bookings_df = pd.DataFrame(
    columns=[
        "Name",
        "Email",
        "Phone Number",
        "ID",
        "Train",
        "Source",
        "Destination",
        "Date",
        "Coach",
    ]
)


# function to book a ticket
def book_ticket(name, email, phone, id_num, train, source, dest, date, coach):
    if available_trains[train][coach] > 0:
        bookings_df.loc[len(bookings_df)] = [
            name,
            email,
            phone,
            id_num,
            train,
            source,
            dest,
            date,
            coach,
        ]
        available_trains[train][coach] -= 1
        return True
    else:
        return False


# function to cancel a ticket
def cancel_ticket(index):
    train = bookings_df.loc[index, "Train"]
    coach = bookings_df.loc[index, "Coach"]
    available_trains[train][coach] += 1
    bookings_df.drop(index, inplace=True)


# main Streamlit app code
st.title(f"Railway Reservation System {st.session_state['user']}")

# view available trains and their seat availability
st.subheader("Available Trains and Seat Availability")
available_trains_df = pd.DataFrame(available_trains)
st.dataframe(available_trains_df)

# book a ticket
st.subheader("Book a Ticket")
name = st.text_input("Name")
email = st.text_input("Email")
phone = st.text_input("Phone Number")
id_num = st.text_input("ID")
train = st.selectbox("Train", list(available_trains.keys()))
source = st.text_input("Source")
dest = st.text_input("Destination")
date = st.date_input("Date")
coach = st.selectbox("Coach", ["1A", "2A", "Sleeper"])
if st.button("Book"):
    if book_ticket(name, email, phone, id_num, train, source, dest, date, coach):
        st.success("Ticket booked successfully!")
    else:
        st.error(
            "Sorry, the selected coach in the selected train is full. Please try again with a different coach or train."
        )

# view booked tickets
st.subheader("Booked Tickets")
bookings_df.reset_index(drop=True, inplace=True)
if not bookings_df.empty:
    st.dataframe(bookings_df)
    cancel_index = st.number_input(
        "Enter the index of the ticket you want to cancel",
        min_value=0,
        max_value=len(bookings_df) - 1,
        value=None,
        step=1,
    )
    if st.button("Cancel Ticket"):
        cancel_ticket(cancel_index)
        st.success("Ticket cancelled successfully!")
else:
    st.info("No tickets booked yet.")
