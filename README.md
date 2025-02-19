# Text Processing API

## About the Task
This project is a RESTful API that processes text using a large language model (LLM). The API can:
- Summarize input text
- Extract keywords
- Perform sentiment analysis

It supports multiple models, including OpenAI GPT-3, GPT-2, and LLaMA, and stores processed results in MongoDB Atlas.

## Code Structure
### 1. `app.py`
- Sets up the Flask API with the following endpoints:
  - `POST /process` → Accepts text input and returns the processed result.
  - `GET /history` → Retrieves previously processed results from MongoDB.
- Handles request validation and response formatting.

### 2. `model.py`
- Defines `LLMProcessor`, a class that loads the selected model and processes text.
- Supports OpenAI GPT-3, GPT-2, and LLaMA via Hugging Face.

### 3. `.env`
Contains environment variables for configuration:
```
LLM_MODEL=""
MONGO_URI=""
OPENAI_API_KEY=""
HUGGINGFACE_TOKEN=""
```

### 4. `requirements.txt`
Lists dependencies required to run the application.

## API Endpoints
### `POST /process`
- **Request Body:**
  ```json
  {"text": "Your input text here"}
  ```
- **Response:**
  ```json
  {
    "summary": "Summarized text...",
    "keywords": ["keyword1", "keyword2"],
    "sentiment": "Positive"
  }
  ```

### `GET /history`
- **Query Parameter:** `limit` (optional, default = 50)
- **Response:**
  ```json
  [
    {"input": "text", "result": {"summary": "...", "keywords": ["..."], "sentiment": "..."}}
  ]
  ```

## Installation Instructions
### 1. Clone the Repository
```sh
git clone https://github.com/hritwij-shrivastava/llm-text-processing.git
cd text-processing-api
```

### 2. Create a Virtual Environment
```sh
pip3 install virtualenv
virtualenv env
```

### 3. Activate the virtual environment in another terminal:
   - For Windows PowerShell:
     ```bash
     .\env\Scripts\activate.ps1
     ```
   - For other terminals:
     ```bash
     source env/bin/activate
     ```

### 4. Install Dependencies
```sh
pip install -r requirements.txt
```

### 5. Set Up Environment Variables
Create a `.env` file and fill in the required values.

### 6. Run the API
```sh
python app.py
```

The API should now be running at `http://127.0.0.1:5000/`.

## Notes
- Ensure you have access to the selected LLM model.
- MongoDB Atlas must be set up and the connection string must be provided in `MONGO_URI`.
- Hugging Face models may require authentication via `HUGGINGFACE_TOKEN`.

