document.addEventListener('DOMContentLoaded', function () {
    const summarizeBtn = document.getElementById('summarizeBtn');
    const resultDiv = document.getElementById('result');
    const loader = document.getElementById('loader');

    summarizeBtn.addEventListener('click', function () {
        chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
            const activeTab = tabs[0];
            const url = activeTab.url;

            // Block non-http pages (chrome://, file://, etc.)
            if (!url || (!url.startsWith('http://') && !url.startsWith('https://'))) {
                resultDiv.innerHTML = '<p class="error">Cannot summarize this page. Please navigate to a regular website.</p>';
                resultDiv.style.display = 'block';
                return;
            }

            // Show loader
            loader.style.display = 'block';
            resultDiv.style.display = 'none';
            summarizeBtn.disabled = true;
            summarizeBtn.querySelector('span').textContent = 'Summarizing...';

            fetch('http://localhost:5000/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            })
            .then(response => {
                // Always parse as JSON — server now guarantees this
                return response.json().then(data => {
                    if (!response.ok) {
                        throw new Error(data.error || 'Server error');
                    }
                    return data;
                });
            })
            .then(data => {
                let html = '';
                if (data.top_image) {
                    html += `<img src="${data.top_image}" class="top-image" onerror="this.style.display='none'">`;
                }
                html += `<h3>${data.title || 'No title found'}</h3>`;
                html += `<div class="meta">By ${data.authors} | ${data.publish_date}</div>`;
                html += `<p>${data.summary || 'No summary available.'}</p>`;
                html += `<span class="sentiment">Sentiment: ${data.sentiment}</span>`;

                resultDiv.innerHTML = html;
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                let msg = error.message;
                // Friendly message if Flask server isn't running
                if (msg.includes('Failed to fetch') || msg.includes('NetworkError')) {
                    msg = 'Cannot connect to the server. Make sure Flask is running on localhost:5000.';
                }
                resultDiv.innerHTML = `<p class="error">Error: ${msg}</p>`;
                resultDiv.style.display = 'block';
            })
            .finally(() => {
                loader.style.display = 'none';
                summarizeBtn.disabled = false;
                summarizeBtn.querySelector('span').textContent = 'Summarize This Page';
            });
        });
    });
});
