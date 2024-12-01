# LISA AI - Student Report Assistant

A Streamlit-based application that uses AI to analyze student documents and generate comprehensive reports.

## Features

- Upload and analyze PDF documents containing student information
- Interactive chat interface to ask questions about the student
- Session management for handling multiple analyses
- Secure document handling with temporary file storage
- AI-powered document analysis using GPT-4

## Setup

1. Create a conda environment:

```bash
conda create -n lisa-ai python=3.10
conda activate lisa-ai
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
```

## Running the Application

1. Activate the conda environment:

```bash
conda activate lisa-ai
```

2. Start the Streamlit app:

```bash
streamlit run app.py
```

3. Open your browser and navigate to the URL shown in the terminal (usually http://localhost:8501)

## Usage

1. Click "Start New Session" to begin
2. Upload a PDF document containing student information
3. Use the chat interface to ask questions about the student
4. Click "End Session" when finished to clean up temporary files

## Notes

- The application uses OpenAI's GPT-4 model for analysis
- Documents are processed using RAG (Retrieval-Augmented Generation)
- Temporary files are automatically cleaned up when sessions end