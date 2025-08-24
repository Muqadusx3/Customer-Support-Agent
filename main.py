from urllib import response
import requests
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()


APPLICATION_TOKEN = os.environ.get("APP_TOKEN")
ENDPOINT = "customer" # The endpoint name of the flow


def run_flow(message: str) -> dict:
    api_url = "https://api.langflow.astra.datastax.com/lf/5459ec2a-1e69-4c07-a84f-accb817953e4/api/v1/run/4454d006-640b-48cf-b570-1f2118475db5"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {
         "Content-Type": "application/json",
        "Authorization": f"Bearer {APPLICATION_TOKEN}",
    }
    try:
        response = requests.request("POST", api_url, json=payload, headers=headers)

        print("Status:", response.status_code)
        print("Raw Response:", response.text)

        if response.status_code != 200:
            raise ValueError(f"Langflow API error: {response.text}")
    
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Request error: {e}")
    except ValueError as ve:
        raise ve

def main():
    st.title("Customer Support Agent")
    
    message = st.text_area("Message", placeholder="Ask something...")
    
    if st.button("Send"):
        if not message.strip():
            st.error("Please enter a message")
            return
    
        try:
            with st.spinner("Sending..."):
                response = run_flow(message)
            
            outputs = response.get("outputs", [])
            if outputs and outputs[0]["outputs"]:
                final_msg = outputs[0]["outputs"][0]["results"]["message"]["text"]
            else:
                final_msg = "No response from Langflow"

            st.markdown(final_msg)
        except Exception as e:
            st.error(str(e))

if __name__ == "__main__":
    main()