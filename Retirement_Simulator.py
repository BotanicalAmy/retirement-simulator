import base64
from pathlib import Path

import streamlit as st
from page_elements import footer, side_content


def linked_image(image_path, page_url):
    b64 = base64.b64encode(Path(image_path).read_bytes()).decode()
    return (
        f'<a href="{page_url}" target="_self">'
        f'<img src="data:image/jpeg;base64,{b64}" style="width:100%; border-radius:4px; cursor:pointer;">'
        f"</a>"
    )


def card_header(title, page_url, bar_color):
    st.html(f"""
<a href="{page_url}" target="_self" style="color:#59579e; text-decoration:none;">
    <h2 style="margin:0 0 6px 0;">{title}</h2>
</a>
<div style="height:15px; background-color:{bar_color}; border-radius:2px; margin:0 0 10px 0;"></div>
""")


st.set_page_config(page_title="Retirement Simulator", page_icon="💵", layout="wide")

st.markdown("# Retirement Simulator")
st.markdown(
    "Design your finances, explore retirement timelines, and forecast "
    "how market conditions shape your future."
)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with st.container(border=True):
        card_header("Design", "/Financial_Design", "#e9e9ee")
        st.markdown(
            "Enter your income, expenses, and savings targets to match your priorities."
        )
        st.markdown(linked_image("images/FinancialDesignSq.jpg", "/Financial_Design"), unsafe_allow_html=True)

with col2:
    with st.container(border=True):
        card_header("Explore", "/Retirement_Explorer", "#c7c2d6")
        st.markdown(
            "Visualize varying retirement scenarios to define a sustainable retirement plan."
        )
        st.markdown(linked_image("images/ExploreSq.jpg", "/Retirement_Explorer"), unsafe_allow_html=True)

with col3:
    with st.container(border=True):
        card_header("Forecast", "/Future_Forecast", "#847f93")
        st.markdown(
            "Run simulations across market scenarios to capture the spread of portfolio outcomes."
        )
        st.markdown(linked_image("images/ForecastSq.jpg", "/Future_Forecast"), unsafe_allow_html=True)

footer()

with st.sidebar:
    side_content()
