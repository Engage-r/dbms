import streamlit as st
import pandas as pd
import psycopg2


# define function to book tickets
def book_ticket(user_id, train_number, source, destination, date, num_seats):
    # do some processing here to book the ticket
    # this is just a dummy implementation for demonstration purposes
    
    conn = psycopg2.connect(
            host="localhost",
            database="t2",
            user="postgres",
            password="password"
    )

    # create a cursor object to execute SQL queries
    cur = conn.cursor()

        # execute the find_trains_btw_stations function to get available trains
    
    cur.execute("SELECT * FROM get_min_avail_seats(%s, %s, %s, %s)", (int(train_number), int(source), int(destination), date))
    available_trains = cur.fetchone()

    if available_trains[0] < num_seats:
        st.write("No seats available!")
        return

    print("SELECT * FROM book_seat(%s, %s, %s, %s, %s, %s)", (int(user_id), int(train_number), int(source), int(destination), date, num_seats))
    cur.execute("SELECT * FROM book_seat(%s, %s, %s, %s, %s, %s)", (int(user_id), int(train_number), int(source), int(destination), date, num_seats))
    available_trains = cur.fetchone()
    # row = cur.fetchone()


    # convert the result to a pandas dataframe and show it in Streamlit
    # print(row)
    print(available_trains)
    print("--------------------------------")



    # close the cursor and database connection
    conn.commit()
    cur.close()
    conn.close()
    
    st.write(
        f"Booking {num_seats} tickets from {source} to {destination} on {date}"
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
    train_number = st.text_input("Enter train number:")
    user_id = st.session_state["user"]
    # show available trains for selected source, destination, and date
    # st.write("Available Trains:")
    # trains_df = pd.read_csv("trains.csv") # assuming the train data is stored in a CSV file
    # available_trains = trains_df[(trains_df["Source"]==source) & (trains_df["Destination"]==destination) & (trains_df["Date"]==date)]
    # st.dataframe(available_trains)

    # book the ticket
    if st.button("Book Ticket"):
        book_ticket(user_id, train_number, source, destination, date, num_seats)


# run the app
if __name__ == "__main__":
    book_ticket_page()
