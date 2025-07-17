import streamlit as st 
from auth_db import csr, conn

st.title("Login Page")

# Initialize session state variables
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# If already logged in
if st.session_state.authenticated:
    st.success(f"Already logged in as {st.session_state.username}")
    st.write("Welcome to the protected page!")
    st.button("Logout", on_click=lambda: logout())

else:
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")

    btn = st.button("Login")

    if btn:
        if username == "" or password == "":
            st.error("Please fill all fields...")
            st.snow()
        else:
            csr.execute(f"SELECT * FROM signup_user WHERE username = %s", (username,))
            user = csr.fetchone()

            if user is None:
                st.warning("Username not found..!")
            elif password != user[4]:
                st.warning("Please enter a valid password")
            else:
                # ✅ Store session state
                st.session_state.authenticated = True
                st.session_state.username = user[1]  # or username
                st.success("Login Successfully done..!")
                st.balloons()
                st.rerun()  # rerun the script to go to "logged in" state

# Optional: Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.rerun()
