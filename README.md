# Northstar Support Assistant

A small customer-support chat demo built with Flask. The app includes a modern support dashboard UI inspired by a customer care workspace and a backend endpoint that returns mock support replies.

## Features
- Chat-style support interface
- Suggestion chips for common support flows
- Responsive layout for desktop and mobile
- Mock support API endpoint for demo conversations
- Minimal Python app ready to run locally or deploy

## Run locally

1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

2. Install dependencies

```bash
python -m pip install -r requirements.txt
```

3. Start the app

```bash
python app.py
```

4. Open the app in your browser

```text
http://127.0.0.1:5000
```

## Project structure

```text
.
├── app.py
├── requirements.txt
├── static/
│   ├── app.js
│   └── styles.css
├── templates/
│   └── index.html
└── README.md
```

## Notes
This is a frontend + demo backend for a customer support assistant. The `/api/chat` endpoint currently returns rule-based responses for common customer service requests. Replace the mock logic in `app.py` with a real AI or help-center backend when you’re ready.
