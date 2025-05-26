# Rival Guru

Want to beat the competition? Start by understanding them. This tool helps you analyze competitors in your market space, track their features, and identify opportunities for differentiation.

## Overview

This project provides a Streamlit-based web application for tracking and analyzing competitors. It allows you to:
- Compare competitor features side-by-side
- Identify market gaps and opportunities
- Generate insights based on collected data

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. Clone this repository
   ```
   git clone <repository-url>
   cd competitor-analysis
   ```

2. Create and activate a virtual environment
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Set up `.env`
```
API_TOKEN= 
WEB_UNLOCKER_ZONE= 
BROWSER_AUTH= 
OPENAI_API_KEY=   
```

5. Run backend server:
```
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

6. Change the backend url in `.streamlit/secret.toml`
```
BACKEND_URL= "http://0.0.0.0:8000"
```

7. Run the Streamlit app
```
streamlit run app.py
```

## Usage

1. Access the application at http://localhost:8501 after starting the server
2. Enter website whose you want to find competitors
3. Compare features and metrics in the analysis dashboard
4. Export reports as needed

## Project Structure

```
competitor-analysis/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Project dependencies
├── .venv/                 # Virtual environment
├── backend/app            # Backend application
│   ├── main.py            # FAST Api webserver
│   └── mcp_client.py
└── README.md              # Project documentation
```