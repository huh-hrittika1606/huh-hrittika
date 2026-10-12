# AI-Powered Customer Support Assistant

A beginner-friendly customer support chatbot that retrieves answers from a small FAQ knowledge base. It demonstrates text cleaning, TF-IDF features, cosine similarity, and a simple response-selection workflow in a Streamlit chat interface.

> **Demo only:** `data/faqs.json` contains fictional sample answers and policies. Replace every sample with current, approved content before showing this to customers. The app does not generate answers or check the accuracy of its knowledge base.

## Features

- Chat-style interface with conversation history for the current browser session
- TF-IDF text vectors and cosine similarity to find a relevant FAQ
- Minimum-match threshold with a clear fallback when no FAQ is close enough
- Displays the selected FAQ and a text-similarity score for transparency
- Local FAQ file; no API key or external AI service required
- Editable JSON knowledge base

## Quick start

Use Python 3.11 or newer.

```bash
# 1. Create and activate a virtual environment
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Start the app
streamlit run app.py
```

Streamlit prints a local URL (usually `http://localhost:8501`) to open in your browser.


## Run it in GitHub Codespaces

This repository includes a Codespaces development setup. From the GitHub repository page:

1. Select **Code** → **Codespaces** → **Create codespace on main**.
2. When the Codespace finishes setting up, open its terminal. Dependencies are installed automatically during setup.
3. Run:

   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```

4. When Codespaces offers to open port **8501**, select **Open in Browser**.

If the port notification does not appear, open the **Ports** panel and open port 8501. Stop the app with `Ctrl+C` when finished, and stop the Codespace when you no longer need the cloud workspace. GitHub Codespaces usage can count toward account quotas or billing.

GitHub Pages cannot run this Python/Streamlit app. For a shareable hosted app URL, deploy the public repository through [Streamlit Community Cloud](https://share.streamlit.io/) and choose `app.py` as the entrypoint.
## How it works

1. The app loads each FAQ question and its keywords from `data/faqs.json`.
2. `TfidfVectorizer` converts those texts into weighted word and two-word features.
3. A customer question is transformed into the same feature space.
4. Cosine similarity ranks the FAQ entries by text overlap.
5. The highest-scoring answer is returned only if its score meets the minimum threshold (`0.18` by default in `support_assistant/engine.py`). Otherwise, the app asks the customer to rephrase or contact support.

The score is a measure of text similarity, **not** a probability that an answer is correct. Tune the threshold with representative example questions before using a real knowledge base.

## Update the knowledge base

Edit `data/faqs.json`. Each record has this structure:

```json
{
  "question": "How do I update my account email?",
  "answer": "Use the account settings page, or contact the support team.",
  "keywords": ["change email address profile account"]
}
```

Keep answers short, specific, and approved by the team that owns the policy. Add alternate wording and customer terms to `keywords` to improve matching. Keep the JSON valid, then restart the app to reload the knowledge base.

## Project layout

```text
.
├── app.py                       # Streamlit user interface
├── data/
│   └── faqs.json                # Sample, editable FAQ content
├── support_assistant/
│   └── engine.py                # FAQ validation and retrieval logic
├── requirements.txt
└── README.md
```

## Limitations and safe use

- This is retrieval-based NLP, not a generative AI model. It can only return answers already in the FAQ file.
- TF-IDF relies on shared words. It can miss paraphrases, misspellings, context, or multi-part questions.
- A high text-similarity score does not guarantee the answer is correct. Review the selected FAQ and test the threshold with realistic queries.
- Do not put customer secrets, credentials, payment information, or sensitive personal data into a public demo. Use approved data handling and hosting practices before any real deployment.
- Replace the sample support email and every sample policy before sharing.

## Next steps

- Add an evaluation set of example questions and expected FAQ matches
- Compare TF-IDF with a sentence-embedding retrieval approach
- Add an admin workflow for reviewing and publishing approved FAQ changes
- Add privacy-aware feedback and human handoff
- Deploy only after reviewing authentication, data retention, privacy, and operational requirements

## Concepts demonstrated

`TfidfVectorizer` builds a weighted text representation and cosine similarity compares the query to FAQ entries. Useful references: [scikit-learn TF-IDF vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html), [scikit-learn cosine similarity](https://scikit-learn.org/stable/modules/metrics.html#cosine-similarity), and [Streamlit chat elements](https://docs.streamlit.io/develop/api-reference/chat).


