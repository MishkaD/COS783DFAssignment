from flask import Flask, request, jsonify
from flask_cors import CORS
from search_engine import search

app = Flask(__name__)
CORS(app)

@app.route("/search", methods=["POST"])
def search_api():
    data = request.json
    query = data.get("query")

    results = search(query)

    return jsonify({
        "query": query,
        "count": len(results),
        "results": results
    })

if __name__ == "__main__":
    app.run(debug=True)