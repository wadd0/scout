import hmac

import streamlit as st

from modules.risk.assessment import build_assessment_chain


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


if not check_password():
    st.stop()

# Main Streamlit app starts here

st.image("assets/ukscout_linear.png", width=350)

with st.form("my_form"):
    st.write("Risk assessment")
    activity = st.text_area(
        label="Activity",
        value=(
            "Pumpkin carving with tee light candles. "
            "Pumpkin carving will be done on tables in groups of 2, 2 groups per table."
        ),
        placeholder="Activity",
    )
    location = st.text_area(
        label="Location",
        value=(
            "The Queens Hall is large brick building with a large room with a hard "
            "wooden floor with stacked chairs around the perimeter."
        ),
        placeholder="Location",
    )

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")

    if submitted:
        with st.spinner("Generating..."):
            result = f"**Activity:** {activity} \n\n **Location:** {location}"
            risk_chain = build_assessment_chain()
            risks = risk_chain.invoke({"activity": activity, "location": location})
            st.markdown(risks.to_markdown())
