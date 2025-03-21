from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests
import json

# Load environment variables
load_dotenv()

# Get API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Please check your .env file.")

app = Flask(__name__)
CORS(app)

@app.get("/")
def index_get():
    return render_template("base.html")

@app.post("/predict")
def predict():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"answer": "Invalid request. Please send a message."}), 400

    user_message = data["message"]
    
    response = get_gemini_response(f"You are an assistant nutrient checker. Can you be a friendly assistant and answer questions like: {user_message}")

    if response is None:
        return jsonify({"answer": "Sorry, I couldn't process the request."}), 500
    
    return jsonify({"answer": response})

def get_gemini_response(question):
    url = f"https:"                         ###
    
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": question}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        response_json = response.json()

        # Debugging response
        print("API Response:", response_json)

        # Extracting response correctly
        if "candidates" in response_json:
            for candidate in response_json["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    return candidate["content"]["parts"][0]["text"]
        
        return "I'm not sure how to answer that right now."

    except Exception as e:
        print("Error:", e)
        return None

if __name__ == "__main__":
    app.run(debug=True)