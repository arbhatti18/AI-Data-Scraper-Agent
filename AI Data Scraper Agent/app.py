
import streamlit as st
import pandas as pd
from scraper import scrape_website

st.set_page_config(
    page_title="AI Website Scraper",
    page_icon="🌐",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: white;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #60a5fa;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #94a3b8;
    margin-bottom: 35px;
}

div.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    height: 48px;
    width: 100%;
    border: none;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">AI Website Intelligence Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Website scraping and business intelligence platform</div>',
    unsafe_allow_html=True
)

st.divider()

st.subheader("Website Analysis")

with st.form("scraper_form"):

    url = st.text_input(
        "Enter Website Domain",
        placeholder="https://techmatetech.com/"
    )

    submitted = st.form_submit_button(
        "🚀 Start Scraping"
    )

if submitted:

    if not url.strip():
        st.error("Please enter a website URL.")

    else:
        with st.spinner("Analyzing website..."):

            try:
                data = scrape_website(url.strip())

                st.success("Website scraped successfully!")

                st.subheader("Website Overview")

                col1, col2 = st.columns(2)

                col1.metric(
                    "Headings Found",
                    len(data["headings"])
                )

                col2.metric(
                    "Paragraphs Found",
                    len(data["paragraphs"])
                )

                st.subheader("Website Information")

                st.write("**Website:**", data["url"])
                st.write("**Title:**", data["title"])

                st.subheader("Headings")
                st.write(data["headings"])

                st.subheader("Extracted Content")
                st.write(data["paragraphs"])

                st.subheader("Website Links")
                st.write(data["links"])

                df = pd.DataFrame([{
                    "Website": data["url"],
                    "Title": data["title"],
                    "Headings": " | ".join(data["headings"]),
                    "Paragraphs": " | ".join(data["paragraphs"]),
                    "Links": " | ".join(data["links"])
                }])

                st.download_button(
                    "Download Scraped Data CSV",
                    df.to_csv(index=False).encode("utf-8-sig"),
                    file_name="website_data.csv",
                    mime="text/csv"
                )

            except Exception as error:
                st.error(f"Scraping failed: {error}")

st.divider()

st.caption("AI Website Intelligence Agent | Built with Python")
