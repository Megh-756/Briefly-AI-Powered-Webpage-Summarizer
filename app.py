from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
import nltk
import os
from textblob import TextBlob
from newspaper import Article
from urllib.parse import urlparse
import validators
from flask_cors import CORS

nltk.download('punkt')
nltk.download('punkt_tab')

app = Flask(__name__)
CORS(app)

def get_website_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def summarize_url(url):
    if not validators.url(url):
        return None, "Invalid URL"

    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
    except Exception as e:
        return None, f"Failed to process article: {str(e)}"

    title = article.title
    authors = ', '.join(article.authors)
    if not authors:
        authors = get_website_name(url)

    publish_date = article.publish_date.strftime('%B %d, %Y') if article.publish_date else "N/A"

    # Use newspaper's built-in NLP summary — far better than manual split
    summary = article.summary if article.summary else ""

    # Fallback: first 5 sentences from article text
    if not summary and article.text:
        sentences = article.text.split('.')
        summary = '.'.join(sentences[:5])

    top_image = article.top_image

    analysis = TextBlob(article.text)
    polarity = analysis.sentiment.polarity

    
    if polarity > 0.15:
        sentiment = 'positive 😊'
    elif polarity < -0.15:
        sentiment = 'negative 😟'
    else:
        sentiment = 'neutral 😐'

    return {
        'title': title,
        'authors': authors,
        'publish_date': publish_date,
        'summary': summary,
        'top_image': top_image,
        'sentiment': sentiment
    }, None


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        data, error = summarize_url(url)

        if error:
            flash(error)
            return redirect(url_for('index'))

        if not data or data['summary'] == "":
            flash('Could not summarize the article.')
            return redirect(url_for('index'))

        return render_template('index.html', **data)

    return render_template('index.html')


@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    url = data['url']
    result, error = summarize_url(url)

    if error:
        return jsonify({'error': error}), 400

    if not result or not result.get('summary'):
        return jsonify({'error': 'Could not summarize the article.'}), 400

    return jsonify(result)


# Global error handler — ensures Flask NEVER returns HTML to the extension
@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({'error': str(e)}), 500


app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

if __name__ == '__main__':
    app.run(debug=True)
