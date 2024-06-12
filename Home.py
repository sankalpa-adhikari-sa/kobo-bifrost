import streamlit as st
import requests
def get_username():
    if "token" in st.session_state or "base_url_v1" in st.session_state :
        headers = {"Authorization": f'Token {st.session_state.token}'}
        url = f"{st.session_state.base_url_v1}/user"
        res= requests.get(url=url, headers=headers)
        if res.status_code==200:
            username= res.json()["username"]
            st.sidebar.success(f"Welcome {username}")

get_username()
st.title("Welcome to _KOBO_-:blue[_Bifrost_]")

st.subheader("#1 Getting Started with KOBO-Bifrost", divider="grey")

"""Before getting started with KOBO-Bifrost you would need base url of KOBO api. The Base URL of the kobo api depends on the server you are currently using, generally they may be:

`Version 1 api` for submission/updates
- https://kc-eu.kobotoolbox.org/api/v1
- https://kc.kobotoolbox.org/api/v1

 `Version 2 api` for Reading/listing
- https://eu.kobotoolbox.org/api/v2
- https://kf.kobotoolbox.org/api/v2


"""
st.subheader("#2 Accessing Token", divider="grey")
"""
You can access your Authorization Token/API key in two ways:

1. Method 1:
 
 Go to Accounts > Security > API Key

2. Method 2:

Navigate to https://eu.kobotoolbox.org/token/?format=json
"""
st.subheader("#3 Accessing Form Id", divider="grey")
"""
Navigate to the project you want to view/add sumbmission this may look like following:
"""
st.code("eu.kobotoolbox.org/#/forms/[FormID]/summary", language="html")
"""
Copy [FormID] which is represents the id of your project/form
"""
