import streamlit as st

# Streamlit config
st.set_page_config(layout="centered")

st.header("Comparing newsletter platforms")

st.write("*How much will it cost to host **my** newsletter?*")

msg = """
Figuring out how much it will cost to host your newsletter on a platform such as [Ghost](https://ghost.org), [Buttondown](https://buttondown.email), [beehiiv](https://www.beehiiv.com), or [Substack](https://substack.com) can be really confusing. This is especially true if you expect your newsletter to grow over time.

This tool can help, by letting you set the parameters that match your situation.
"""

# msg = "If you're trying to figure out where to host an email newsletter on a platform such as Ghost or Substack, it can be really confusing to figure out how much it might cost. This is especially true if you expect your newsletter to grow. This tool can help."
st.info(msg)

if st.button("Compare platforms", type="primary"):
    st.switch_page("pages/nl_compare.py")

st.write("---")

st.write("##### Why is pricing dificult?")

msg = "There are a number of reasons it's hard to figure out how much a newsletter hosting service will actually cost:"
st.write(msg)

msg = """
- The number of subscribers is likely to change, so you're not just looking at one price.
- Your revenue depends on a number of factors:
    - How many subscribers you have;
    - How many of your subscribers have paid subscriptions;
    - Your average annual revenue per paid subscriber depends on things like discounts and promotions. It's usually not as simple as "$5 per month per paid user", or anything like that.
"""
st.write(msg)
