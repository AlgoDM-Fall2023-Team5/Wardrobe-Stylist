import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
try:
    firebase_admin.get_app()
except ValueError:
    cred = credentials.Certificate(r"D:\Projects\ADM Project Final\Wardrobe-Stylist\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)




# Streamlit App
def main():
    st.title("Create New User Account")

    # Input fields
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")
    display_name = st.text_input("Display Name:")

    # Button to create user
    if st.button("Create User"):
        # Create a new user
        try:
            user = auth.create_user(email=email, password=password, display_name=display_name)
            st.success(f"User created successfully: {user.uid}")
        except ValueError:
            st.error(f"Error creating user: ")

if __name__ == "__main__":
    main()
