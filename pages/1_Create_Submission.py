from pygwalker.api.streamlit import StreamlitRenderer
import requests
import pandas as pd
import os
import argparse
import streamlit as st
 
def row_to_json(row):
    result = {}
    for col in row.index:
        if '/' in col:
            prefix, key = col.split('/', 1)
            if prefix not in result:
                result[prefix] = {}
            result[prefix][key] = row[col]
        else:
            result[col] = row[col]
    return result


lis=[]
def make_requests(dataframe,form_id):
    if "token" in st.session_state or "base_url_v1" in st.session_state:
        headers = {"Authorization": f'Token {st.session_state.token}'}
        url= f"{st.session_state.base_url_v1}/submissions"
        
        df = pd.read_excel(dataframe)
        df.fillna("", inplace=True)
        json_list = df.apply(row_to_json, axis=1).tolist()
        progress_bar= st.progress(0,text="Submiting data....")
        is_success=0

        for i in range(len(json_list)):
            data={
            "id": form_id,
            "submission": json_list[i],
            "meta":{
            "_submitted_by": "csisa_allhub", 
        
            }}
            
            try:
                res = requests.post(url=url, headers=headers, params={"format": "json"} ,json=data)
                
                if res.status_code ==201:
                    # st.toast(f":green[status code: {res.status_code} /n {res.json()["message"]}]", icon="✅")
                    is_success+=1
                elif res.status_code == 202:
                    is_success+=1
                    st.toast(f":blue[status code: {res.status_code} /n {res.json()["error"]}]", icon="ℹ️")
                else: 
                    st.toast(f":orange[status code: {res.status_code} /n {res.json()["error"]}]", icon="🚨")
                    lis.append(json_list[i])
            except:
                st.toast(":orange[something went wrong, Please make sure URL, Token, Form Id are correct and excel file is attached]", icon="🚨")
                lis.append(json_list[i])
            progress_bar.progress((i+1)/len(json_list), text=f"Submiting data({is_success}/{len(json_list)})....")
    else: pass
    
    
def show_error_rows():
         st.subheader("Unsuccessful Submission")
         """
         Submission may fail due to one of following reasons:
         - Incorrect form ID, 
         - Invalid KOBO api url (check which server you are currently using)
         - Invalid Token
         
         """
         data= pd.json_normalize(st.session_state.unsuccessful_rows)
         st.dataframe(data,use_container_width=True)





         

def get_username():
    if "token" in st.session_state or "base_url_v1" in st.session_state :
        headers = {"Authorization": f'Token {st.session_state.token}'}
        url = f"{st.session_state.base_url_v1}/user"
        res= requests.get(url=url, headers=headers)
        if res.status_code==200:
            username= res.json()["username"]
            st.sidebar.success(f"Welcome {username}")

get_username()
kobo_form=st.form("kobo_form")
# KOBO form
form_id= kobo_form.text_input("Form Id", type="default", key="form_id")
uploaded_file = kobo_form.file_uploader("Choose a file", key="uploaded_file")


submit_form= kobo_form.form_submit_button("Submit to Server" )

if submit_form :
    if (st.session_state.base_url_v1 =="" or st.session_state.token=="" or st.session_state.form_id=="" or st.session_state.uploaded_file == None):
        st.error("Please provide URL, TOKEN, Form ID, and Excel File",icon="🚨")
    else: 
        make_requests(dataframe=uploaded_file, form_id=form_id)
        
        st.session_state.unsuccessful_rows = lis

    



if 'unsuccessful_rows_btn' not in st.session_state:
    st.session_state.unsuccessful_rows_btn = False

def toggle_button():
    st.session_state.unsuccessful_rows_btn = not st.session_state.unsuccessful_rows_btn

st.button('Unsuccessful Submission', on_click=toggle_button)

if st.session_state.unsuccessful_rows_btn:
    try:
        show_error_rows()
    except: pass
else:
    pass
