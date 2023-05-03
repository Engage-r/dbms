import streamlit as st
import bcrypt

st.set_page_config(
    page_title="Railway Reservation System - Login",
    page_icon=":train:",
    layout="centered",
)


# Define the layout of the page
def login():
    st.title("Login")
    st.write("Please enter your login details below.")

    # Get the user's email address
    email = st.text_input("Email address")

    # Get the user's password
    password = st.text_input("Password", type="password")

    # Login the user if they submit the form
    if st.button("Login"):
        # Open the file containing the user credentials
        with open("users.txt", "r") as f:
            # Loop through the lines in the file to find the user's credentials
            for line in f:
                # Split the line into its components
                name, stored_email, stored_password = line.strip().split(", ")

                # Check if the email and password match the stored credentials
                if email == stored_email and bcrypt.checkpw(
                    password.encode("utf-8"), stored_password.encode("utf-8")
                ):
                    st.success("You have successfully logged in!")
                    return

        st.error("Incorrect email address or password. Please try again.")


login()
