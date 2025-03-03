import streamlit as st


def test_select():
    files = ["file1.txt", "file2.txt"]

    st.session_state.current_book = files[0]
    print(st.session_state.current_book)
    selected_book = st.sidebar.selectbox(
        "Select a book:",
        files,
        index=files.index(st.session_state.current_book),
    )

    st.session_state.current_book = selected_book
    print(st.session_state.current_book)
    print("===========")


def test_num_input():
    if "current_page" not in st.session_state:
        st.session_state.current_page = 0
    page_number = st.number_input(
        "Go to page:",
        min_value=1,
        max_value=50,
        value=st.session_state.current_page + 1,
        step=1,
        label_visibility="collapsed",
    )
    if st.session_state.current_page != page_number - 1:
        st.session_state.current_page = page_number - 1
        st.rerun()
    print(st.session_state.current_page)


def test_text_input():
    def clear():
        st.session_state.user_question = ""

    user_question = st.text_input(
        "Ask a question about the book", key="user_question", on_change=clear
    )


test_text_input()
