# Project brief: AI-Powered Customer Support Assistant

## Goal
Build an approachable FAQ-based assistant that turns a user's question into a relevant response from an approved knowledge base.

## MVP scope
- Load authorized FAQ/support content from a structured local dataset.
- Clean and structure text.
- Explore introductory NLP concepts.
- Represent text using TF-IDF.
- Match a query to relevant information using cosine similarity.
- Apply a minimum match threshold and provide a safe fallback.
- Present the response in a simple chat interface.

## Out of scope for the MVP
- Generating new policy answers
- Production customer data or live support integrations
- Authentication, monitoring, or production deployment
- Claiming similarity scores are answer-confidence probabilities

## Suggested milestones
1. Run the app with the sample dataset.
2. Replace sample FAQs with a small approved dataset.
3. Collect representative queries and inspect incorrect matches.
4. Tune keywords and the fallback threshold.
5. Compare retrieval approaches and add evaluation before considering deployment.

