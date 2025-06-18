import streamlit as st

# Pages editor
page_1 = st.Page("main.py", title="tips analysis", icon=":material/circle:")
page_2 = st.Page("first_page.py", title="stock analysis", icon=":material/circle:")

pg = st.navigation([page_1, page_2])

# Edir browser title and label
st.set_page_config(page_title="Data manager", page_icon=":material/keyboard_double_arrow_down:")
pg.run()