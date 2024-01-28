import streamlit as st


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

st.write("##### Why is pricing difficult?")

msg = "There are a number of reasons it's hard to figure out how much a newsletter hosting service will actually cost:"
st.write(msg)

msg = """
- The number of subscribers is likely to change, so you're not just considering one fixed price.
- Your revenue depends on a number of factors:
    - How many subscribers you have;
    - How many of your subscribers have paid subscriptions;
    - The average revenue per paid subscriber depends on things like discounts, promotions, and montly vs annual plans. It's not as simple as"$5 per month per paid user".
"""
st.write(msg)

msg = """
This tool lets you set the **number of subscribers**, your **percentage of paid subscribers**, and your **average annual revenue per paid subscriber**.

You'll then be able to directly compare the costs associated with all platforms, for your unique situation.
"""
st.info(msg)

st.write("(To get started, click the *Compare platforms* button above.)")

st.write("---")


# Sidebar.
st.sidebar.header("About")

msg = """
This project was developed by [Eric Matthes](https://fosstodon.org/@ehmatthes).

I write a weekly newsletter called [Mostly Python](https://www.mostlypython.com). If you're a Python programmer, please check it out. (It's currently hosted on Substack, but I'll be using Ghost starting in late February.)
"""
st.sidebar.write(msg)

st.sidebar.write("---")

msg = """
If you find anything broken or notice any inaccuracies here, please [open an issue](https://github.com/ehmatthes/nl_analyzer) and I'll be happy to address it.

I'm also happy to hear any [feedback](https://github.com/ehmatthes/nl_analyzer) about how this has helped you decide which platform to use, or any suggestions for what might be more helpful. 
"""
st.sidebar.write(msg)
