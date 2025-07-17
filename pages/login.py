import streamlit as st 
from auth_db import csr, conn

st.title("Login Page")

username = st.text_input("Enter your username")

password = st.text_input("Enter your password",type = "password" )

btn = st.button("Login")

if btn:
    if username == "" or password == "":
        st.error("Please fill all fields...")
        st.snow()
    
    else:
        csr.execute(f"select * from signup_user where username = '{username}';")
        
        check_usernmae = csr.fetchone()

        if check_usernmae is None:
            st.warning("Username not found..!")
        
        else:

            if password != check_usernmae[4]:
                st.warning("Please enter valid password")

            else:
                st.write(check_usernmae)
                st.write(f"you suvessfuly login as {check_usernmae[1]}")
                st.success("Login Sucessfully done..!")
                st.balloons()