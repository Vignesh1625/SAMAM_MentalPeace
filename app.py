import streamlit as st

# Read the html file
with open("index.html", "r") as f:
    html_content = f.read()

# Display the html content
st.markdown(html_content, unsafe_allow_html=True)
