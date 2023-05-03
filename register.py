import streamlit as st
import bcrypt

st.set_page_config(
    page_title="Railway Reservation System - Register",
    page_icon=":train:",
    layout="centered",
)


# Define the layout of the page
def register():
    st.title("Register")
    st.write("Please enter your details below to register.")

    # Get the user's name
    name = st.text_input("Name")

    # Get the user's email address
    email = st.text_input("Email address")

    # Get the user's password
    password = st.text_input("Password", type="password")

    # Get the user's type
    user_type = st.selectbox("User type", ["Admin", "User"])

    # Register the user if they submit the form
    if st.button("Register"):
        # Hash the user's password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Open the file where we'll store the user's credentials
        with open("users.txt", "a") as f:
            # Write the user's details to the file, including the hashed password
            f.write(f"{name}, {email}, {hashed_password.decode('utf-8')}\n")

        # Open the file where we'll store the user's type
        with open("user_types.txt", "a") as f:
            # Write the user's email and type to the file
            f.write(f"{email}, {user_type}\n")

        st.success("You have successfully registered!")


register()
