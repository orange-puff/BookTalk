import streamlit as st
import os
import glob
import fitz  # PyMuPDF
from openai import OpenAI
import io
from PIL import Image

# Initialize OpenAI client
os.environ["OPENAI_API_KEY"] = open("open-ai-api-key").read().strip()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Set page config
st.set_page_config(layout="wide")

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_page" not in st.session_state:
    st.session_state.current_page = 0
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False


# Function to load PDF content
def load_pdf(file_path):
    return fitz.open(file_path)


# Function to render PDF page
def render_page(pdf_doc, page_num):
    page = pdf_doc[page_num]
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    return img


# Function to extract text from a page
def extract_text(pdf_doc, page_num):
    page = pdf_doc[page_num]
    return page.get_text()


# Function to generate response from OpenAI
def generate_response(prompt):
    # Get current page text for context
    pdf_doc = load_pdf(st.session_state.current_book)
    current_page_text = extract_text(pdf_doc, st.session_state.current_page)

    # Build context from chat history
    context = ""
    for q, a in st.session_state.chat_history:
        context += f"Q: {q}\nA: {a}\n\n"

    # Final prompt with context
    final_prompt = f"Previous conversation:\n{context}\n\nCurrent page content:\n{current_page_text}\n\nQuestion: {prompt}"

    response = client.chat.completions.create(
        model="gpt-4-turbo", messages=[{"role": "user", "content": final_prompt}]
    )

    return response.choices[0].message.content


# Function to toggle chat window
def toggle_chat():
    st.session_state.show_chat = not st.session_state.show_chat


# Function to handle next page
def next_page():
    pdf_doc = load_pdf(st.session_state.current_book)
    if st.session_state.current_page < len(pdf_doc) - 1:
        st.session_state.current_page += 1


# Function to handle previous page
def prev_page():
    if st.session_state.current_page > 0:
        st.session_state.current_page -= 1


# Main app
def main():
    st.title("Book Talk App")

    # Get list of PDF files in current directory
    pdf_files = glob.glob("*.pdf")

    if not pdf_files:
        st.error("No PDF files found in the current directory.")
        return

    # Book selection dropdown
    if (
        "current_book" not in st.session_state
        or st.session_state.current_book not in pdf_files
    ):
        st.session_state.current_book = pdf_files[0]
        st.session_state.current_page = 0

    selected_book = st.sidebar.selectbox(
        "Select a book:",
        pdf_files,
        index=pdf_files.index(st.session_state.current_book),
    )

    if selected_book != st.session_state.current_book:
        st.session_state.current_book = selected_book
        st.session_state.current_page = 0
        st.session_state.chat_history = []

    # Toggle chat button
    st.sidebar.button("Toggle Chat", on_click=toggle_chat)

    # Load PDF
    pdf_doc = load_pdf(st.session_state.current_book)

    # Layout based on chat visibility
    if st.session_state.show_chat:
        col1, col2 = st.columns([2, 1])

        with col1:
            # PDF viewer
            st.image(
                render_page(pdf_doc, st.session_state.current_page),
                use_container_width=True,
            )

            # Page navigation
            col_prev, col_next = st.columns(2)
            with col_prev:
                if st.button("← Previous Page"):
                    prev_page()
            with col_next:
                if st.button("Next Page →"):
                    next_page()

            st.write(f"Page {st.session_state.current_page + 1} of {len(pdf_doc)}")

        with col2:
            # Chat interface
            st.subheader("Chat")

            # Display chat history
            for question, answer in st.session_state.chat_history:
                st.write(f"**You:** {question}")
                st.write(f"**AI:** {answer}")
                st.write("---")

            # User input
            user_question = st.text_input("Ask a question about the book")
            if st.button("Send"):
                if user_question:
                    # Generate response
                    response = generate_response(user_question)

                    # Update chat history
                    st.session_state.chat_history.append((user_question, response))

                    # Clear input
                    st.rerun()
    else:
        # Full width PDF viewer
        st.image(
            render_page(pdf_doc, st.session_state.current_page),
            use_container_width=True,
        )

        # Page navigation
        col_prev, col_next = st.columns(2)
        with col_prev:
            if st.button("← Previous Page"):
                prev_page()
        with col_next:
            if st.button("Next Page →"):
                next_page()

        st.write(f"Page {st.session_state.current_page + 1} of {len(pdf_doc)}")


if __name__ == "__main__":
    main()
