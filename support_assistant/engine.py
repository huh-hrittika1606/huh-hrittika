"""FAQ retrieval engine using TF-IDF and cosine similarity."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DEFAULT_MIN_MATCH_SCORE = 0.18
FALLBACK_ANSWER = (
    "I couldn't find a reliable answer in the current FAQ. "
    "Please rephrase your question or contact the support team."
)


@dataclass(frozen=True)
class MatchResult:
    answer: str
    matched_question: str | None
    score: float
    matched: bool


class FAQAssistant:
    """Find the FAQ whose wording is most similar to a customer question."""

    def __init__(
        self,
        faqs: list[dict[str, Any]],
        min_match_score: float = DEFAULT_MIN_MATCH_SCORE,
    ) -> None:
        if not faqs:
            raise ValueError("The FAQ knowledge base must contain at least one entry.")
        if not 0 <= min_match_score <= 1:
            raise ValueError("min_match_score must be between 0 and 1.")

        self.faqs = [self._validate_faq(item, index) for index, item in enumerate(faqs, 1)]
        self.min_match_score = min_match_score
        documents = [self._document_text(item) for item in self.faqs]
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), strip_accents="unicode")
        self.faq_vectors = self.vectorizer.fit_transform(documents)

    @staticmethod
    def _validate_faq(item: Any, index: int) -> dict[str, Any]:
        if not isinstance(item, dict):
            raise ValueError(f"FAQ entry {index} must be an object.")
        question = item.get("question")
        answer = item.get("answer")
        keywords = item.get("keywords", [])
        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"FAQ entry {index} needs a non-empty question.")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError(f"FAQ entry {index} needs a non-empty answer.")
        if not isinstance(keywords, list) or not all(isinstance(word, str) for word in keywords):
            raise ValueError(f"FAQ entry {index} keywords must be a list of strings.")
        return {"question": question.strip(), "answer": answer.strip(), "keywords": keywords}

    @staticmethod
    def _document_text(faq: dict[str, Any]) -> str:
        return " ".join([faq["question"], *faq["keywords"]])

    @classmethod
    def from_json(cls, path: str | Path, min_match_score: float = DEFAULT_MIN_MATCH_SCORE) -> "FAQAssistant":
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("The FAQ JSON file must contain a list of FAQ objects.")
        return cls(data, min_match_score=min_match_score)

    def answer(self, query: str) -> MatchResult:
        """Return the closest answer only when the text match clears the threshold."""
        if not isinstance(query, str) or not query.strip():
            return MatchResult(FALLBACK_ANSWER, None, 0.0, False)

        query_vector = self.vectorizer.transform([query.strip()])
        scores = cosine_similarity(query_vector, self.faq_vectors).ravel()
        best_index = int(scores.argmax())
        score = float(scores[best_index])
        best_faq = self.faqs[best_index]

        if score < self.min_match_score:
            return MatchResult(FALLBACK_ANSWER, None, score, False)

        return MatchResult(best_faq["answer"], best_faq["question"], score, True)

