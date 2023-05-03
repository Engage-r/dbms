import streamlit as st
import bcrypt

st.set_page_config(
    page_title="Railway Reservation System", page_icon=":train:", layout="centered"
)


# Define the layout of the page
def welcome():
    st.title("Welcome to the Railway Reservation System")
    st.write("Please select an option below to continue.")

    # Create buttons for login and register
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            # Redirect the user to the login page
            st.experimental_set_query_params(page="login")
    with col2:
        if st.button("Register"):
            # Redirect the user to the register page
            st.experimental_set_query_params(page="register")
    # Get the query parameters from the URL

    # Check if the "page" parameter is set to "login"


def login():
    st.title("Login")
    st.write("Please enter your login details below.")

    # Get the user's email address
    email = st.text_input("Email address")

    # Get the user's password
    password = st.text_input("Password", type="password")

    # Login the user if they submit the form
    if st.button("Sign in"):
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
                    st.session_state["user"] = "in"
                    return
        st.session_state["user"] = "out"
        st.error("Incorrect email address or password. Please try again.")


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
    if st.button("Sign Up"):
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


if __name__ == "__main__":
    welcome()
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "login":
        login()
    if "page" in query_params and query_params["page"][0] == "register":
        register()
