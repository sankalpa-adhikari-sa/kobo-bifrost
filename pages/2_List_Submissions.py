import streamlit as st
import pandas as pd
import requests

def get_json_data():
     if "token" in st.session_state or "base_url_v2" in st.session_state or "form_listing_id" in st.session_state :
        headers = {"Authorization": f'Token {st.session_state.token}'}
        url=f"{st.session_state.base_url_v2}/assets/{st.session_state.form_listing_id}/data/?format=json"
        try:
            res = requests.get(url=url, headers=headers)
            
            if res.status_code ==200: 
                st.toast(f":green[Successly fetched data]", icon="✅")
                fetched_data= pd.json_normalize(res.json()["results"])
                fetched_data_df= st.dataframe(fetched_data)
                


            elif res.status_code == 202:
        
                st.toast(f":blue[status code: {res.status_code} /n {res.json()['error']}]", icon="ℹ️")
            else: 
                st.toast(f":orange[status code: {res.status_code} /n {res.json()['error']}]", icon="🚨")
            return fetched_data_df

        except:
            st.toast(":orange[something went wrong, Please make sure URL, Token, Form Id are correct and excel file is attached]", icon="🚨")
     else: pass
def get_username():
    if "token" in st.session_state or "base_url_v1" in st.session_state :
        headers = {"Authorization": f'Token {st.session_state.token}'}
        url = f"{st.session_state.base_url_v1}/user"
        res= requests.get(url=url, headers=headers)
        if res.status_code==200:
            username= res.json()["username"]
            st.sidebar.success(f"Welcome {username}")

get_username()
kobo_listings=st.form("kobo_listings")
form_id= kobo_listings.text_input("Form Id", type="default")
submit_form= kobo_listings.form_submit_button("View Submissions" )

if submit_form:
    if form_id == "" :
        st.error("Please provide Form ID to view submissions",icon="🚨")
    else: 
        st.session_state.form_listing_id = form_id
        st.toast("Added Form Id for listing")

    if "token" in st.session_state and "base_url_v2" in st.session_state and "form_listing_id" in st.session_state :
        get_json_data()
    else:
        st.info("Please Enter KOBO Credentials for listing the submission", icon="ℹ️")
