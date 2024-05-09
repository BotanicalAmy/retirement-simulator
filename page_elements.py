import streamlit as st
import streamlit.components.v1 as components

#creating reusable footer for the app
def footer():
    st.divider()
    st.image('images/mountainbg.jpg')
    st.write("""Created by [Denver Data Design](https://denverdatadesign.com/) 
             | Follow Amy on [LinkedIn](https://www.linkedin.com/in/amy-folkestad-76873884/) 
             | See her work on [GitHub](https://github.com/BotanicalAmy)""")
    st.markdown('''*The retirement predictions created by this application are for educational and enterainment purposes. 
                While data science can deliver probable results, the future can never be forecasted with certainty.*''')

def side_content():
    st.markdown('**Denver Data Design**')
    st.write("Add some information about my services?")
    st.write("Create a link to a post about building a Streamlit app?")
    #adding space
    st.markdown('#')
    buy_me_flower = '''
    <script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="BotanicalAmy" 
    data-color="#6174bc" data-emoji="🌷"  data-font="Cookie" data-text="Buy me a flower" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
    '''
    components.html(buy_me_flower)