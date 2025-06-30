import streamlit as st
import requests
from bs4 import BeautifulSoup


st.set_page_config(page_title="DubiCars Spec Extractor", layout="wide")
st.title("🚗 DubiCars Spec Extractor")

# Input URL
url = st.text_input("Paste DubiCars listing URL here", "")

if url:
    st.info("Fetching car specifications...")

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        specs = {}
        spec_list = soup.select("ul.faq__data > li")

        if spec_list:
            for li in spec_list:
                spans = li.find_all("span")
                if len(spans) == 2:
                    key = spans[0].get_text(strip=True)
                    value = spans[1].get_text(strip=True)
                    specs[key] = value

            if specs:
                st.success("✅ Extracted Specifications")
                for key, value in specs.items():
                    st.markdown(f"**{key}:** {value}")
            else:
                st.warning("Specs section found but it's empty.")
        else:
            st.error("❌ Could not find the specs section.")

    except Exception as e:
        st.error("🚨 An error occurred while scraping:")
        st.text(str(e))

