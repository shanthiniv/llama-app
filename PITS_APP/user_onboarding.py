import streamlit as st
import os
import pdfplumber
from session_functions import save_session
from logging_functions import log_action
from global_settings import STORAGE_PATH, INDEX_STORAGE

def show_first_two_pages(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            num_pages = min(2, len(pdf.pages))
            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                text = page.extract_text()
                if text:
                    st.write(text)
                else:
                    st.write("No text found on this page.")
    except Exception as e:
        st.error(f"Error reading {file_path}: {e}")

def user_onboarding():
    # Ensure necessary directories exist
    os.makedirs(STORAGE_PATH, exist_ok=True)
    os.makedirs(INDEX_STORAGE, exist_ok=True)

    user_name = st.text_input('What is your name?')
    if not user_name:
        return

    st.session_state['user_name'] = user_name
    st.write(f"Hello {user_name}. It's nice meeting you!")
    
    study_subject = st.text_input('What subject would you like to study?')
    if not study_subject:
        return

    st.session_state['study_subject'] = study_subject
    st.write(f"Okay {user_name}, let's focus on {study_subject}.")
    
    study_goal = st.text_input(
        'Detail any specific goal for your study or just leave it blank:', 
        key='Study Goal'
    )
    st.session_state['study_goal'] = study_goal or "No specific goal"
    
    if study_goal:
        st.write("Do you want to upload any study materials?")
        uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True)
        finish_upload = st.button('FINISH UPLOAD')
        
        st.write("Upload the book or materials file (will not be processed):")
        dummy_uploaded_files = st.file_uploader("Choose book files", accept_multiple_files=True, key="dummy_files")
        finish_dummy_upload = st.button('FINISH BOOK UPLOAD')

        if finish_upload and uploaded_files:
            saved_file_names = []

            for uploaded_file in uploaded_files:
                file_path = os.path.join(STORAGE_PATH, uploaded_file.name)
                try:
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    saved_file_names.append(uploaded_file.name)
                    st.write(f"You have uploaded {uploaded_file.name}")
                except Exception as e:
                    st.error(f"Error uploading file {uploaded_file.name}: {e}")

            st.session_state['uploaded_files'] = saved_file_names
            st.session_state['finish_upload'] = True
            st.info('Uploading files...')

        if finish_dummy_upload and dummy_uploaded_files:
            for dummy_file in dummy_uploaded_files:
                st.write(f"Dummy file {dummy_file.name} has been uploaded.")

    if 'finish_upload' in st.session_state or 'difficulty_level' in st.session_state:
        st.write('Please select your current knowledge level on the topic')
        difficulty_level = st.radio(
            'Current knowledge:', 
            ['Beginner', 'Intermediate', 'Advanced', 'Take a quiz to assess'],
        )
        st.session_state['difficulty_level'] = difficulty_level
        proceed_button = st.button('Proceed')
        st.write(f'Your choice: {difficulty_level}')
        
        if proceed_button:
            save_session(st.session_state)
            for file_name in st.session_state.get('uploaded_files', []):
                st.write(f"First two pages of {file_name}:")
                show_first_two_pages(os.path.join(STORAGE_PATH, file_name))

if __name__ == "__main__":
    # Set your API key here
    os.environ['OPENAI_API_KEY'] = "sk-None-c55Aikf60LUmG7IrZWrbT3BlbkFJeIhPXFFyz7CxbAsbdIwu"
    user_onboarding()
