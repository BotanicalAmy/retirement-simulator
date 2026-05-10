import streamlit as st
import base64

#creating reusable footer for the app
def footer():
    st.divider()
    st.write("""Created by [Denver Data Design](https://denverdatadesign.com/)
             | Follow Amy on [LinkedIn](https://www.linkedin.com/in/amy-folkestad-76873884/) 
             | See her work on [GitHub](https://github.com/BotanicalAmy)""")
    st.markdown('''*The retirement predictions created by this application are for educational and enterainment purposes. 
                While applied mathematics can deliver probable results, past performance is not indicative of future returns.*''')

def V_SPACE(lines):
    for _ in range(lines):
        st.write('&nbsp;')

def retirement_inputs():
    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown('**What is your initial investment?**')
        investment_str = st.text_input(label="Initial investment", label_visibility="collapsed", placeholder='e.g. 50,000')
        investment = None
        if investment_str:
            try:
                investment = int(float(investment_str.replace(',', '').replace('$', '').strip()))
                if investment < 1000:
                    st.warning("Value must be at least $1,000")
                    investment = None
            except ValueError:
                st.error("Please enter a valid number")

        st.markdown('**What will your annual contribution be?**')
        contribution_str = st.text_input(label="Annual contribution", label_visibility="collapsed", placeholder='e.g. 5,000 (optional)')
        contribution = 0
        if contribution_str:
            try:
                contribution = int(float(contribution_str.replace(',', '').replace('$', '').strip()))
            except ValueError:
                st.error("Please enter a valid number")
                contribution = 0

    with col2:
        st.markdown('**What type of investor are you?**')
        investor = st.selectbox('Investor type', ('Moderate', 'Aggressive', 'Conservative'), label_visibility="collapsed")

        st.markdown('**Select a retirement withdrawal rate**')
        percent = st.selectbox('Withdrawal rate', ['3%', '4%', '5%', '6%'], index=1, label_visibility="collapsed")
        withdrawl_rate = float(percent.strip('%')) / 100

    with col3:
        st.markdown('**How many years until you retire?**')
        years = st.slider('Years until retirement', 0, 50, 20, label_visibility="collapsed")
        st.markdown("""
        <style>
        section[data-testid="stMain"] .stButton > button {
            background-color: #59579e !important;
            color: white !important;
            border: none !important;
            margin-top: 30px !important;
        }
        section[data-testid="stMain"] .stButton > button:hover {
            background-color: #645c77 !important;
            color: white !important;
        }
        @media (max-width: 768px) {
            section[data-testid="stMain"] .stButton > button {
                margin-top: 0px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        forecast_clicked = st.button("Forecast your Future")

    return investment, contribution, investor, years, percent, withdrawl_rate, forecast_clicked


def side_content():
    with open('images/DenverDataLogo.png', 'rb') as f:
        logo_b64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
<style>
[data-testid="stDataFrame"] th {{
    background-color: #f7f7f9 !important;
    color: #374151 !important;
}}
[data-testid="stDataFrame"] [col-id="0"] {{
    color: #374151 !important;
}}
[data-testid="stSidebarNavLink"] {{
    font-weight: bold !important;
    font-size: 1rem !important;
    text-decoration: none !important;
    color: #374151 !important;
}}
[data-testid="stSidebarNavLink"] span {{
    font-weight: bold !important;
    font-size: 1rem !important;
    color: #374151 !important;
}}
[data-testid="stSidebarNavLink"][aria-current="page"],
[data-testid="stSidebarNavLink"][aria-current="page"] span {{
    color: #59579e !important;
}}
[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNavLink"]:hover span {{
    color: #645c77 !important;
}}
[data-testid="stSidebarNav"]::before {{
    content: '';
    display: block;
    background-image: url('data:image/png;base64,{logo_b64}');
    background-repeat: no-repeat;
    background-size: contain;
    background-position: center;
    width: 100%;
    height: 150px;
    margin-bottom: 20px;
}}
.logo-link-overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 22rem;
    height: 170px;
    z-index: 1000;
    display: block;
    cursor: pointer;
}}
</style>
<a href="https://denverdatadesign.com" target="_blank" class="logo-link-overlay"></a>
""", unsafe_allow_html=True)
    st.markdown('<strong>Denver Data Design</strong>', unsafe_allow_html=True)
    st.markdown('''Amy is a data engineer and technical leader with a background in applied math and statistics. Built for an AI course, this simulator ultimately worked better with applied math.''')
    st.markdown('''<a href="https://denverdatadesign.com/about-amy/" target="_blank"
        onmouseover="this.style.color='#645c77'" onmouseout="this.style.color='#59579e'"
        style="color:#59579e; font-weight:bold; text-decoration:none;">
        About Amy</a>''', unsafe_allow_html=True)


