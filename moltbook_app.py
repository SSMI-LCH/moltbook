import streamlit as st
import moltbook_crawling
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Moltbook Crawler",
    page_icon="🦞",
    layout="wide"
)

st.title("🦞 Moltbook Crawler App")
st.write("Click the button below to crawl content from **moltbook.com**.")

# Sidebar for options
st.sidebar.header("Options")
headless_mode = st.sidebar.checkbox("Headless Mode", value=True, help="Run browser in background")

if st.button("Start Crawling", type="primary"):
    with st.spinner("Crawling Moltbook... This may take a few seconds."):
        try:
            # clean previously displayed data? Streamlit reruns the script on interaction, so variables reset unless in session_state.
            # But here we just run it on button click.
            
            data = moltbook_crawling.crawl_moltbook(headless=headless_mode)
            
            if data:
                st.success(f"Successfully crawled {len(data)} items!")
                
                # Display data
                for item in data:
                    with st.container():
                        st.markdown("---")
                        st.subheader(f"{item['id'] + 1}. {item['title']}")
                        st.write(item['description'])
                        with st.expander("View Raw HTML"):
                            st.code(item['html'], language="html")
            else:
                st.warning("No items found. The website structure might have changed.")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")
st.caption("Moltbook Crawler | Built with Selenium & Streamlit")
