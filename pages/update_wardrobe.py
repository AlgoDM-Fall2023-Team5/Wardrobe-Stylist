import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth

# Initialize Firebase Admin SDK
try:
    firebase_admin.get_app()
except ValueError:
    # Initialize Firebase only if it's not already initialized
    cred = credentials.Certificate(r"D:\Projects\ADM Project Final\Wardrobe-Stylist\serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Streamlit App
def main():
    st.title("Retrieve User UID by Email and Password")

    # Input fields
    email = st.text_input("Email:")
    password = st.text_input("Password:", type="password")

    # Button to retrieve user UID
    if st.button("Retrieve User UID"):
        try:
            # Sign in the user
            login= auth.sign_in_with_email_and_password(email,password)
            user = auth.get_user_by_email(email)
            
            # Check if the entered password is correct
            # auth.verify_password(user.uid, password)
            
            st.success(f"User UID: {user.uid}")

        except ValueError as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
