import re
import requests
from flask import Flask, jsonify

app = Flask(__name__)

def get_latest_time_stories():
    url = "http://www.time.com"
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        stories = extract_stories(html_content)
        return stories[:6]
    else:
        return []

def extract_stories(html_content):
    # Identify the HTML elements that contain the latest stories.
    story_pattern = r'<li class="latest-stories__item">\s+<a href="(.*?)">\s+<h3 class="latest-stories__item-headline">(.*?)</h3>\s+</a>\s+<time class="latest-stories__item-timestamp">.*?</time>\s+</li>'
    stories = re.findall(story_pattern, html_content, re.DOTALL)

    # Extract the necessary information from the matched elements.
    latest_stories = []
    for url, title in stories:
        latest_stories.append({
            "title": title.strip(),
            "link": "https://time.com"+url,
        })

    return latest_stories

@app.route('/getTimeStories', methods=['GET'])
def get_time_stories():
    latest_stories = get_latest_time_stories()
    return jsonify(latest_stories)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
