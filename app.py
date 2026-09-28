import random
import time

import streamlit as st

from randselect import selector

st.set_page_config(page_title="randselect")
st.title("randselect")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "result" not in st.session_state:
    st.session_state.result = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("Names")
    with st.form("add_name_form", clear_on_submit=True):
        new_name = st.text_input("Add a name")
        if st.form_submit_button("Add") and new_name.strip():
            st.session_state.names.append(new_name.strip())
    for name in st.session_state.names:
        st.write(f"- {name}")

with col2:
    st.subheader("Questions")
    with st.form("add_question_form", clear_on_submit=True):
        new_question = st.text_input("Add a question")
        if st.form_submit_button("Add") and new_question.strip():
            st.session_state.questions.append(new_question.strip())
    for question in st.session_state.questions:
        st.write(f"- {question}")

st.divider()

no_repeats = st.checkbox("No repeats (this session)")
draw_disabled = not st.session_state.names or not st.session_state.questions
draw_clicked = st.button("Draw", disabled=draw_disabled)

if draw_clicked:
    placeholder = st.empty()
    start = time.time()
    while time.time() - start < 3:
        flash_name = random.choice(st.session_state.names)
        flash_question = random.choice(st.session_state.questions)
        placeholder.markdown(f"### {flash_name} — {flash_question}")
        time.sleep(0.1)

    if no_repeats:
        name_pool = selector.available_choices(st.session_state.names, st.session_state.used_names)
        if len(name_pool) == len(st.session_state.names) and st.session_state.used_names:
            st.session_state.used_names = set()
        question_pool = selector.available_choices(st.session_state.questions, st.session_state.used_questions)
        if len(question_pool) == len(st.session_state.questions) and st.session_state.used_questions:
            st.session_state.used_questions = set()
    else:
        name_pool = st.session_state.names
        question_pool = st.session_state.questions

    chosen_name, chosen_question = selector.random_selection(name_pool, question_pool)

    if no_repeats:
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)

    st.session_state.result = (chosen_name, chosen_question)
    placeholder.empty()

if st.session_state.result:
    chosen_name, chosen_question = st.session_state.result
    st.success(f"{chosen_name}, please answer: {chosen_question}")
