import streamlit as st
import bcrypt
import psycopg2

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
    email_id = st.text_input("Email address")

    # Get the user's password
    password = st.text_input("Password", type="password")

    # Login the user if they submit the form
    if st.button("Sign in"):
        # Open the file containing the user credentials
        conn = psycopg2.connect(
            host="localhost",
            database="t2",
            user="postgres",
            password="password"
        )
        
        cur = conn.cursor()

        # Execute a SQL query to check if the username and password match a record in the database
        cur.execute("SELECT * FROM users WHERE email_id = %s", (email_id,))

        # Fetch the first row returned by the query
        row = cur.fetchone()

        # print(row)
        # print("===============================")

        if row is not None:
            print("Login successful")
            st.success("You have successfully logged in!")
            st.session_state["user"] = row[0]
            return

        st.error("Incorrect email address or password. Please try again.")
        
        st.session_state["user"] = "out"
        # Close the cursor and database connection
        cur.close()
        conn.close()


def register():
    st.title("Register")
    st.write("Please enter your details below to register.")

    # Get the user's name
    username = st.text_input("Username")

    # Get the user's email address
    email_id = st.text_input("Email address")

    age = st.text_input("Age")
    
    mobile_no = st.text_input("Mobile Number")


    # Get the user's password
    password = st.text_input("Password", type="password")

    # Get the user's type
    user_type = st.selectbox("User type", ["Admin", "User"])

    # Register the user if they submit the form
    if st.button("Sign Up"):
        # Hash the user's password using bcrypt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Open the file where we'll store the user's credentials

        conn = psycopg2.connect(
            host="localhost",
            database="t2",
            user="postgres",
            password="password"
        )
        cur = conn.cursor()

        # check if the email address already exists in the database
        cur.execute("SELECT COUNT(*) FROM users WHERE email_id=%s", (email_id,))
        count = cur.fetchone()[0]
        if count > 0:
            st.write("An account with this email address already exists.")
        else:
            # insert the new user's data into the database
            cur.execute("INSERT INTO users (username, email_id, age, mobile_no) VALUES (%s, %s, %s, %s)", (username, email_id, age, mobile_no))
            conn.commit()
            st.write("You have successfully registered.")
        st.success("You have successfully registered!")


if __name__ == "__main__":
    welcome()
    query_params = st.experimental_get_query_params()
    if "page" in query_params and query_params["page"][0] == "login":
        login()
    if "page" in query_params and query_params["page"][0] == "register":
        register()
