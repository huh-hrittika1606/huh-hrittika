"""Chat interface for the sample FAQ retrieval assistant."""
from __future__ import annotations

from pathlib import Path

import streamlit as st

from support_assistant.engine import FAQAssistant

PROJECT_ROOT = Path(__file__).resolve().parent
FAQ_PATH = PROJECT_ROOT / "data" / "faqs.json"

st.set_page_config(
    page_title="Customer Support Assistant",
    page_icon="💬",
    layout="centered",
)

st.markdown(
    """
    <style>
      .block-container { max-width: 880px; padding-top: 2.5rem; }
      [data-testid="stChatMessage"] { border-radius: 14px; }
      .demo-note { padding: 0.85rem 1rem; border-left: 4px solid #75b798;
                   background: rgba(117, 183, 152, 0.10); border-radius: 5px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 Customer Support Assistant")
st.caption("A beginner-friendly FAQ assistant powered by text similarity.")
st.markdown(
    '<div class="demo-note"><strong>Demo knowledge base:</strong> '
    "The included shop FAQs and policies are examples. Replace them with approved, "
    "current support content before using this with customers.</div>",
    unsafe_allow_html=True,
)

try:
    assistant = FAQAssistant.from_json(FAQ_PATH)
except (OSError, ValueError) as exc:
    st.error(f"Could not load the FAQ knowledge base: {exc}")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About this demo")
    st.write("Questions are matched to the closest FAQ with TF-IDF and cosine similarity.")
    st.write("No external AI service or API key is used.")
    st.caption("Similarity scores are not confidence probabilities.")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("match"):
            st.caption(
                f"Matched FAQ: {message['match']} · "
                f"Text similarity: {message['score']:.0%} (not a probability)"
            )
        elif message["role"] == "assistant":
            st.caption("No FAQ cleared the match threshold.")

if not st.session_state.messages:
    st.markdown("**Try a question**")
    st.markdown(
        "- How can I track my order?\n"
        "- What is your return policy?\n"
        "- How do I reset my password?"
    )

prompt = st.chat_input("Ask a question about the sample shop…", max_chars=500)
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    result = assistant.answer(prompt)
    assistant_message = {"role": "assistant", "content": result.answer}
    if result.matched:
        assistant_message["match"] = result.matched_question
        assistant_message["score"] = result.score
    else:
        assistant_message["score"] = result.score
    st.session_state.messages.append(assistant_message)
    st.rerun()


