import re
import streamlit as st
import pandas as pd


def is_valid_website(name):
    pattern = re.compile(
        r"^(?:https?://)?"
        r"(?:www\.)?"
        r"([a-zA-Z0-9-]{1,63}\.)+"
        r"[a-zA-Z]{2,}$"
    )
    return bool(pattern.match(name))


def render_rivals():
    st.markdown("Here is competitor analysis:")

    # Sample data
    data = {
        "Description": [
            "E-commerce giant",
            "Search engine company",
            "Social media platform",
        ],
        "Category": ["Retail", "Technology", "Social Media"],
        "Year Founded": [1994, 1998, 2004],
        "Employees": [1500000, 156500, 77805],
        "Annual Revenue": ["$514B", "$282B", "$117B"],
        "Global Rank": [3, 1, 4],
        "Visits": ["2.7B monthly", "90B monthly", "1.9B daily"],
        "Bounce Rate": ["32%", "28%", "45%"],
        "Avg Visit Duration": ["7:12", "9:50", "19:30"],
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Display the table
    st.dataframe(df, use_container_width=True)


def main():
    st.title("Rival Guru ⚔")
    st.markdown(
        "<h6>Want to beat your rivals? Start by understanding them. Rival Guru helps to know your competitors.</h6>",
        unsafe_allow_html=True,
    )
    st.divider()

    website = st.text_input("👉 What's your website name?", placeholder="microsoft.com")
    if website:
        if not is_valid_website(website):
            st.error("Please enter a valid website name.")
            return
        render_rivals()


if __name__ == "__main__":
    main()
