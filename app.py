from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
import nltk
from textblob import TextBlob
from newspaper import Article
from datetime import datetime
from urllib.parse import urlparse
import validators
import requests
from flask_cors import CORS

nltk.download('punkt')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def get_website_name(url):
    # Extract the website name from the URL
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith("www."):
        domain = domain[4:]
    return domain

def summarize_url(url):
    if not validators.url(url):
        return None, "Invalid URL"

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None, "Failed to download content"

    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    title = article.title
    authors = ', '.join(article.authors)
    if not authors:
        authors = get_website_name(url)
    publish_date = article.publish_date.strftime('%B %d, %Y') if article.publish_date else "N/A"

    article_text = article.text
    sentences = article_text.split('.')
    max_summarized_sentences = 5
    summary = '.'.join(sentences[:max_summarized_sentences])

    top_image = article.top_image

    analysis = TextBlob(article.text)
    polarity = analysis.sentiment.polarity

    if polarity > 0:
        sentiment = 'happy 😊'
    elif polarity < 0:
        sentiment = ' sad 😟'
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
    
    return jsonify(result)

app.secret_key = 'your_secret_key'

if __name__ == '__main__':
    app.run(debug=True)