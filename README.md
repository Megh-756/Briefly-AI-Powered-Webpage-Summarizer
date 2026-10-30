# Briefly

**An AI-powered browser extension that turns lengthy online articles into concise, readable summaries.**

Briefly is a web-based article summarization tool with a browser extension that allows users to summarize the webpage they are currently viewing. It extracts article content, generates a concise summary, and performs sentiment analysis to give readers a quick understanding of the article.

## Overview

Reading lengthy articles, blogs, and news reports can be time-consuming. Briefly addresses this by extracting the main content from a webpage and presenting its key information in a shorter format.

The project consists of two connected components:

- **Flask Backend:** Handles article extraction, summarization, sentiment analysis, and API requests.
- **Browser Extension:** Allows users to submit the URL of their current webpage without manually copying it into the web application.

The backend processes the submitted URL using `newspaper3k`, extracts the article's content and metadata, generates a summary, and evaluates its sentiment using TextBlob.

## Key Features

- **One-Click Article Summarization:** Summarize the currently opened webpage through the browser extension.
- **Content Extraction:** Extract article titles, authors, publication dates, images, and main text.
- **Automatic Summarization:** Generate concise summaries using newspaper3k's NLP functionality.
- **Sentiment Analysis:** Classify article sentiment as Positive, Negative, or Neutral.
- **Web-Based Interface:** Submit article URLs directly through the Flask application.
- **REST API:** Expose article summarization functionality through a JSON endpoint.
- **Error Handling:** Handle invalid URLs, inaccessible articles, and unsuccessful extraction requests.

## How It Works

1. The user opens an article and activates the Briefly browser extension.
2. The extension sends the webpage URL to the Flask backend.
3. The backend validates the URL and downloads the article.
4. `newspaper3k` extracts the article's title, authors, publication date, image, and text.
5. The extracted content is processed to generate a concise summary.
6. TextBlob calculates sentiment polarity from the article text.
7. The backend returns the summary, metadata, and sentiment classification.
8. The browser extension or web interface displays the results.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Backend Framework | Flask |
| Article Extraction | newspaper3k |
| Natural Language Processing | NLTK |
| Sentiment Analysis | TextBlob |
| URL Validation | validators |
| Cross-Origin Requests | Flask-CORS |
| Frontend | HTML, CSS, JavaScript |
| Browser Integration | Browser Extension APIs |

## Project Structure

```text
Briefly/
│
├── extension/
│   └── Browser extension source files
│
├── static/
│   └── CSS and static assets
│
├── templates/
│   └── Flask HTML templates
│
├── app.py
│   └── Flask application, extraction,
│       summarization and API logic
│
├── requirements.txt
│   └── Python dependencies
│
├── .gitignore
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9 or later
- pip
- Google Chrome or Microsoft Edge
- Internet connection

### 1. Clone the Repository

```bash
git clone https://github.com/Megh-756/Briefly.git
cd Briefly
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

The application downloads the required NLTK resources during startup. An internet connection is required for the initial download.

### 4. Start the Backend

```bash
python app.py
```

The Flask application will be available at:

`http://127.0.0.1:5000/`

Keep the backend running while using the browser extension.

## Browser Extension Setup

Briefly can be loaded locally as an unpacked browser extension.

1. Open your browser's extension management page.
2. For Chrome, navigate to `chrome://extensions`.
3. For Edge, navigate to `edge://extensions`.
4. Enable **Developer Mode**.
5. Click **Load unpacked**.
6. Select the `extension/` folder from the cloned repository.
7. Pin Briefly to the browser toolbar.
8. Open an article and select **Summarize This Page**.

The extension communicates with the locally running Flask backend, so the backend must remain active.

## API Reference

Briefly provides an endpoint for submitting article URLs programmatically.

### POST `/api/summarize`

**Request Body:**

```json
{
  "url": "https://example.com/article"
}
```

**Example Request:**

```bash
curl -X POST http://127.0.0.1:5000/api/summarize \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com/article"}'
```

**Response Structure:**

```json
{
  "title": "Article Title",
  "authors": "Author Name",
  "publish_date": "January 01, 2025",
  "summary": "A concise summary of the article.",
  "top_image": "https://example.com/image.jpg",
  "sentiment": "positive 😊"
}
```

The example values are illustrative. Actual response data depends on the article and the metadata available from its source.

## Implementation Details

### Article Extraction and Summarization

The `newspaper3k` library handles article downloading, parsing, metadata extraction, and NLP summarization.

If the library does not generate a summary but article text is available, the application falls back to extracting the first five sentence segments.

### Sentiment Analysis

TextBlob calculates the polarity of the extracted article text.

The application uses the following thresholds:

| Polarity | Classification |
|---|---|
| Greater than 0.15 | Positive |
| Less than -0.15 | Negative |
| Between -0.15 and 0.15 | Neutral |

This provides a lightweight sentiment estimate rather than a comprehensive interpretation of the article.

## Limitations

- Some websites restrict automated extraction or require JavaScript rendering.
- Article metadata may be incomplete or unavailable.
- Sentiment analysis is based on TextBlob polarity and may not understand sarcasm or contextual meaning.
- The application requires internet access to retrieve articles.
- The Flask development server is intended for local development rather than production deployment.

## Future Improvements

- Introduce more advanced summarization models.
- Allow users to select summary length.
- Improve extraction from JavaScript-rendered websites.
- Add support for additional browsers.
- Improve sentiment analysis accuracy.
- Add automated testing and production deployment configuration.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
