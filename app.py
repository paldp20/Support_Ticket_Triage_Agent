# ui

import streamlit as st
import requests

api = "http://localhost:8000/triage"   # FastAPI endpoint

st.title("Vikara Support Ticket Triage Agent")

desc = st.text_area("Enter description:", height=150)

if st.button("Submit"):
    if not desc.strip():
        st.error("Please enter desc before submitting.")
    else:
        try:
            response = requests.post(api, json={"description": desc})
            if response.status_code == 200:
                data = response.json()
                st.subheader("Model Response")
                next_action = data.get("next_action", "No next action found.")
                st.success(next_action)
            else:
                st.error(f"API error: {response.text}")
        except Exception as e:
            st.error(f"Connection error: {e}")
