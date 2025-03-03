# Book Talk

A Streamlit application that allows you to read PDF books and chat with an AI assistant about the content.

## Features

- PDF book reader with page navigation
- AI-powered chat interface using OpenAI's API
- Toggle chat window for focused reading
- Book selection dropdown for all PDFs in the directory

## Setup

1. Make sure you have Python installed
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
3. Set your OpenAI API key as an environment variable:
   ```
   export OPENAI_API_KEY="your-api-key-here"
   ```

## Running the App

Run the app with the following command:
```
streamlit run app.py
```

## Usage

1. Select a book from the dropdown in the sidebar
2. Use the "Toggle Chat" button to show/hide the chat interface
3. Navigate through pages using the "Previous Page" and "Next Page" buttons
4. When the chat window is open, you can ask questions about the content
5. The AI assistant will provide answers based on the current page and previous conversation