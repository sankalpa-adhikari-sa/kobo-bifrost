import streamlit as st
import requests
st.subheader("Add Required credentials")
"""
These credentianls will not be saved between the brower instances. You may require to re-enter the credentials after every page reloads/new instances.
"""
def get_username():
    if "token" in st.session_state or "base_url_v1" in st.session_state :
        headers = {"Authorization": f'Token {st.session_state.token}'}
        url = f"{st.session_state.base_url_v1}/user"
        res= requests.get(url=url, headers=headers)
        if res.status_code==200:
            username= res.json()["username"]
            st.sidebar.success(f"Welcome {username}")

get_username()

kobo_settings=st.form("kobo_settings")
token= kobo_settings.text_input("Token", type="password")
base_url_v1= kobo_settings.text_input("V1 url(create/update/delete)", type="default")
base_url_v2= kobo_settings.text_input("V2 url(read)", type="default")
submit_form= kobo_settings.form_submit_button("Add data" )

if submit_form :
    if (token =="" or base_url_v1=="" or base_url_v2=="" ):
        st.error("Please provide URL, TOKEN",icon="🚨")
    else: 
        st.toast(f":green[Successly added KOBO credentials]", icon="✅")
        if 'token' not in st.session_state:
            st.session_state.token = token
        if 'base_url_v1' not in st.session_state:
            st.session_state.base_url_v1 = base_url_v1
        if 'base_url_v2' not in st.session_state:
            st.session_state.base_url_v2 = base_url_v2
        