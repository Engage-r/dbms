import streamlit as st


def show_train_route():
    # Define the train route for each train number
    train_routes = {
        "12345": ["Station A", "Station B", "Station C"],
        "67890": ["Station X", "Station Y", "Station Z"],
        "24680": ["Station P", "Station Q", "Station R", "Station S"],
    }

    # Get the train number from the user
    train_number = st.text_input("Enter train number:")

    # Show the train route if the user has entered a valid train number
    if train_number in train_routes:
        st.write(f"Train route for train number {train_number}:")
        st.write("```\n" + "\n".join(train_routes[train_number]) + "\n```")
    elif train_number:
        st.error("Invalid train number. Please try again.")


# Create a page to show the train route
st.title("Train Route")
show_train_route()
