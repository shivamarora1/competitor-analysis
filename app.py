import json
import re
import streamlit as st
import pandas as pd
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

st.set_page_config(layout="wide")
if "data" not in st.session_state:
    st.session_state.data = {}

if "loading" not in st.session_state:
    st.session_state.loading = False

if "error" not in st.session_state:
    st.session_state.error = ""


def is_valid_website(name):
    pattern = re.compile(
        r"^(?:https?://)?"
        r"(?:www\.)?"
        r"([a-zA-Z0-9-]{1,63}\.)+"
        r"[a-zA-Z]{2,}$"
    )
    return bool(pattern.match(name))


def render_rivals(website):
    if not website:
        st.session_state.error = "Please enter a website name."
        return
        
    if not is_valid_website(website):
        st.session_state.error = "Please enter a valid website name."
        return
    try:
        st.session_state.loading = True
        response = requests.get(f"{st.secrets['BACKEND_URL']}/scrape/{website}")
        response.raise_for_status()  # Raise exception for non-200 status codes
        data = response.json()
        
        # Validate required fields in the response
        if "company" not in data or "competitors" not in data:
            raise ValueError("API response missing required fields")
            
        st.session_state.data = data
        st.session_state.loading = False
    except requests.exceptions.RequestException as e:
        st.session_state.error = f"API request failed: {str(e)}"
        st.session_state.loading = False
        st.session_state.data = {}
    except (ValueError, json.JSONDecodeError) as e:
        st.session_state.error = f"Invalid data received: {str(e)}"
        st.session_state.loading = False
        st.session_state.data = {}
    except Exception as e:
        st.session_state.error = "Something went wrong. Please try again later."
        st.session_state.loading = False
        st.session_state.data = {}


def main():
    st.title("Rival Guru ⚔")
    st.markdown(
        "<h6>Want to beat your rivals? Start by understanding them. Rival Guru helps to know your competitors.</h6>",
        unsafe_allow_html=True,
    )
    st.divider()

    website = st.text_input("👉 What's your website name?", placeholder="microsoft.com")
    btn = st.button("Submit", on_click=render_rivals, args=(website,))

    if st.session_state.loading:
        with st.spinner("Scraping data... This may take a moment."):
            st.empty()
    else:
        if st.session_state.data:
            st.success("Here is your competitor analysis:")
            company = st.session_state.data.get("company", {})
            competitors_data = st.session_state.data.get("competitors", [])
            company_competitors = company.get("competitors", [])
            
            rows = {}
            for i, comp in enumerate(competitors_data):
                if i < len(company_competitors):
                    competitor_name = company_competitors[i].capitalize()
                    rows[competitor_name] = {
                        "Description": comp.get("description", "N/A"),
                        "Category": comp.get("category", "N/A").replace("/", ">", -1),
                        "Year Founded": comp.get("year_founded", "N/A"),
                        "Employees": comp.get("employees", "N/A"),
                        "Annual Revenue": comp.get("annual_revenue", "N/A"),
                        "Global Rank": comp.get("global_rank", "N/A"),
                        "Visits": comp.get("visits", "N/A"),
                        "Bounce Rate": comp.get("bounce_rate", "N/A"),
                        "Avg Visit Duration": comp.get("avg_visit_duration", "N/A"),
                    }
            # Create dataframe if we have data
            if rows:
                df = pd.DataFrame.from_dict(rows, orient="index")
                df_melt = df.reset_index().melt(
                    id_vars="index", var_name="Metric", value_name="Value"
                )
                df_pivot = df_melt.pivot(index="Metric", columns="index", values="Value")
                st.dataframe(df_pivot)
            else:
                st.warning("No competitor data available to display.")

    if st.session_state.error:
        st.error(st.session_state.error)
        st.session_state.error = ""


if __name__ == "__main__":
    main()
