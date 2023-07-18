"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

# Magic commands implicitly
# call st.write().
'_This_ is some **Markdown***'

'dataframe:', df
# st.text('Heading')
# st.markdown('_Markdown_')
# st.write('Apple')
# st.write(['st', 'is <', 3]) # returns a list
# st.title('Title Page')
# st.header('My header')
# st.subheader('My sub')
# st.code('for i in range(8): foo()') # Returns in the code format
# st.dataframe(df)
# st.table(df.iloc[0:2])
# st.json({'foo':'bar','fu':'ba'})
# st.metric('My metric', 42, 2)
img = 'https://30days.streamlit.app/~/+/media/c1d64cbe224f2a71943d37c5294f12c656d9379b6b866e3f418fe9aa.png'
st.image(img)
a = st.sidebar.radio('Select one:', [1, 2])
if a == 1:
    st.write('# one')
    # Three different columns:
    col1, col2, col3 = st.columns([3, 1, 1])
    # col1 is larger.

    # You can also use "with" notation:
    # with col1:
    #     st.radio('Select one :', [1, 2])
    # with col2:
    #     st.radio('Select 2 :', [1, 2])
    # tab1, tab2 = st.tabs(["Tab 1", "Tab2"])
    # tab1.write("this is tab 1")
    #
    # if tab2:
    #     tab2.write("this is tab 2")
    #     st.radio('apple', [2.54, 25.12])
    with st.form(key='my_form'):
        username= st.text_input('Username')
        password = st.text_input('Password')
        st.form_submit_button('Login')
# st.experimental_rerun()
if a == 2:
    st.write('two')
    # col1, col2 = st.columns(2)
    # col1.write('heelo')
    # col2.write('world')
    st.table({'apple': [1, 2, 3], 'ban': [2, 3, 4]})
