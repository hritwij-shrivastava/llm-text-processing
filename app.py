from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import re
import os
from model import LLMProcessor

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MongoDB Atlas Connection
client = MongoClient(os.getenv("MONGO_URI"))
db = client.text_processing
history_collection = db.history

# Get LLM model choice from environment variable
LLM_MODEL = os.getenv("LLM_MODEL", "openai-gpt3")

processor = LLMProcessor(LLM_MODEL)

def extract_keywords(text):
    """Extract keywords using a simple regex approach."""
    words = re.findall(r'\b\w{5,}\b', text)
    return list(set(words))[:10]

@app.route('/process', methods=['POST'])
def process_text():
    """Processes input text and returns summarization, keywords, and sentiment analysis."""
    data = request.get_json()
    if 'text' not in data or not isinstance(data['text'], str) or len(data['text'].strip()) == 0:
        return jsonify({"error": "Invalid input. Please provide a non-empty text field."}), 400
    
    text = data['text']
    
    # Perform summarization
    summary_prompt = f"Summarize the following text briefly:\n\n{text}"
    summary = processor.call_model(summary_prompt)
    
    # Extract keywords
    keywords = extract_keywords(text)
    
    # Perform sentiment analysis
    sentiment_prompt = f"Analyze the sentiment of this text (Positive, Neutral, Negative):\n\n{text}"
    sentiment = processor.call_model(sentiment_prompt)
    
    result = {"summary": summary, "keywords": keywords, "sentiment": sentiment}
    
    # Store in MongoDB
    history_collection.insert_one({"input": text, "result": result})
    
    return jsonify(result)

@app.route('/history', methods=['GET'])
def get_history():
    """Returns the last N processed results from MongoDB."""
    limit = int(request.args.get("limit", 50))  # Default limit to 50
    history = list(history_collection.find({}, {"_id": 0}).sort("_id", -1).limit(limit))
    return jsonify(history)

if __name__ == '__main__':
    app.run(debug=True)
