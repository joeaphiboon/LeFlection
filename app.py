import streamlit as st
import pandas as pd
import json
from datetime import datetime
import os

# Set page config
st.set_page_config(layout="wide", page_title="Learning Reflection App")

# File to store reflections
REFLECTIONS_FILE = "reflections.json"

def load_reflections():
    if os.path.exists(REFLECTIONS_FILE):
        with open(REFLECTIONS_FILE, "r") as f:
            return json.load(f)
    return []

def save_reflection(date, topic, reflection):
    reflections = load_reflections()
    reflections.append({
        "date": date,
        "topic": topic,
        "reflection": reflection
    })
    with open(REFLECTIONS_FILE, "w") as f:
        json.dump(reflections, f)

def get_reflections_df():
    reflections = load_reflections()
    return pd.DataFrame(reflections)

st.title('Learning Reflection App')

# Input form
st.header('Add a New Reflection')

# Use session state to manage form inputs
if 'date' not in st.session_state:
    st.session_state.date = datetime.now()
if 'topic' not in st.session_state:
    st.session_state.topic = ''
if 'reflection' not in st.session_state:
    st.session_state.reflection = ''

date = st.date_input('Date', st.session_state.date)
topic = st.text_input('Topic', st.session_state.topic)
reflection = st.text_area('Reflection', st.session_state.reflection)

if st.button('Submit Reflection'):
    save_reflection(date.strftime('%Y-%m-%d'), topic, reflection)
    st.success('Reflection added successfully!')
    # Clear the input fields
    st.session_state.date = datetime.now()
    st.session_state.topic = ''
    st.session_state.reflection = ''

# View reflections
st.header('View Reflections')
reflections_df = get_reflections_df()

if not reflections_df.empty:
    # Search functionality
    search_term = st.text_input('Search reflections')
    if search_term:
        filtered_df = reflections_df[reflections_df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
    else:
        filtered_df = reflections_df

    # Display reflections
    selected_rows = st.multiselect('Select reflections to remove', filtered_df.index)
    if selected_rows:
        reflections = load_reflections()
        for row in selected_rows[::-1]:
            reflections.pop(row)
        with open(REFLECTIONS_FILE, "w") as f:
            json.dump(reflections, f)
        st.success('Selected reflections removed successfully!')
        # Refresh the page to show updated reflections
        st.query_params.clear()

    st.dataframe(filtered_df)

    # Export to CSV
    if st.button('Export to CSV'):
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="learning_reflections.csv",
            mime="text/csv"
        )

    # Clear button
    if st.button('Clear All'):
        if os.path.exists(REFLECTIONS_FILE):
            os.remove(REFLECTIONS_FILE)

        st.success('All reflections cleared successfully!')
        # Refresh the page to show updated reflections
        st.query_params.clear()
else:
    st.write('No reflections found.')

# Instructions
st.sidebar.header('Instructions')
st.sidebar.markdown("""
1. Add new reflections using the form.
2. View and search your reflections in the table.
3. Select reflections to remove and click the 'Remove' button.
4. Export your reflections to a CSV file, which can be opened in Google Sheets or other spreadsheet software.
5. Your reflections are stored locally in a file named 'reflections.json'.
6. Input fields will clear automatically after submitting a reflection or deleting reflections.
""")