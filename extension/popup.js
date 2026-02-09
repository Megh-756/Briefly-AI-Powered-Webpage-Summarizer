document.addEventListener('DOMContentLoaded', function() {
    const summarizeBtn = document.getElementById('summarizeBtn');
    const resultDiv = document.getElementById('result');
    const loader = document.getElementById('loader');

    summarizeBtn.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            const activeTab = tabs[0];
            const url = activeTab.url;

            if (!url) {
                resultDiv.innerHTML = '<p class="error">Cannot get URL of active tab.</p>';
                resultDiv.style.display = 'block';
                return;
            }

            // Show loader, hide result and button
            loader.style.display = 'block';
            resultDiv.style.display = 'none';
            summarizeBtn.disabled = true;
            summarizeBtn.textContent = 'Summarizing...';

            fetch('http://localhost:5000/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({url: url})
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => { throw new Error(err.error || 'Network response was not ok'); });
                }
                return response.json();
            })
            .then(data => {
                let html = '';
                if (data.top_image) {
                    html += `<img src="${data.top_image}" class="top-image">`;
                }
                html += `<h3>${data.title}</h3>`;
                html += `<div class="meta">By ${data.authors} | ${data.publish_date}</div>`;
                html += `<p>${data.summary}</p>`;
                html += `<span class="sentiment">Sentiment: ${data.sentiment}</span>`;
                
                resultDiv.innerHTML = html;
                resultDiv.style.display = 'block';
            })
            .catch(error => {
                resultDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
                resultDiv.style.display = 'block';
            })
            .finally(() => {
                loader.style.display = 'none';
                summarizeBtn.disabled = false;
                summarizeBtn.textContent = 'Summarize This Page';
            });
        });
    });
});
