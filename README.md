# Briefly - AI News Summarizer & Browser Extension

Briefly is a Python-based web application and browser extension that automatically summarizes news articles and analyzes their sentiment using Artificial Intelligence. It leverages `requests`, `newspaper3k`, `TextBlob`, and `NLTK` to extract key information (title, authors, publication date, top image) and provide a concise summary along with sentiment analysis (Happy, Sad, Neutral).

## How to Run

### 1. Backend Setup (Flask Server)

1.  **Install dependencies**:
    Ensure you have Python installed, then run:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the application**:
    ```bash
    python app.py
    ```
    The server will start at `http://127.0.0.1:5000/`.

### 2. Browser Extension Setup

1.  **Open your browser's extension management page**:
    - **Chrome/Edge**: Go to `chrome://extensions` or `edge://extensions`.
    - **Firefox**: Go to `about:debugging#/runtime/this-firefox`.

2.  **Enable Developer Mode**:
    - Toggle the "Developer mode" switch (usually in the top right corner).

3.  **Load the Extension**:
    - Click **Load unpacked**.
    - Select the `extension` folder inside this project directory.

4.  **Use the Extension**:
    - Pin the Briefly extension to your toolbar.
    - Navigate to any news article.
    - Click the Briefly icon and hit "Summarize This Page".

> **Note:** The Flask backend (`python app.py`) must be running for the extension to work.
