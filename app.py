from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Replace with your own YouTube Data API v3 key
YOUTUBE_API_KEY ="AIzaSyCbPdvJmfbJ0Er8PTrMSdiewjAQGMD2x88"

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("q", "")
    if not query:
        return jsonify([])

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "videoCategoryId": "10",    # Music category
        "videoEmbeddable": "true",  # Only embeddable videos
        "maxResults": 15,
        "key": YOUTUBE_API_KEY
    }

    r = requests.get(YOUTUBE_SEARCH_URL, params=params)
    data = r.json()

    results = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        channel = item["snippet"]["channelTitle"]
        thumbnail = item["snippet"]["thumbnails"]["medium"]["url"]
        results.append({
            "videoId": video_id,
            "title": title,
            "channel": channel,
            "thumbnail": thumbnail
        })

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)
