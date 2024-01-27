import streamlit as st



st.header("Comparing newsletter platforms")

msg = "If you're looking at the various platforms available for hosting an email newsletter, it can be really confusing to figure out how much it might cost, especially as your newsletter grows. This tool can help."
st.write(msg)

if st.button("Compare platforms"):
    st.switch_page("pages/nl_compare.py")
