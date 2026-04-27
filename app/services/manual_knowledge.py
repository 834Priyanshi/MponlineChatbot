from __future__ import annotations

from typing import Any

MANUAL_KNOWLEDGE: list[dict[str, Any]] = [
    {
        "keywords": ["register", "registration", "sign up", "create account"],
        "answer": (
            "To use MPOnline, first create an account on the official portal. "
            "Then log in with your email and password to access services, view status, and raise requests."
        ),
        "sources": ["Manual knowledge base"],
    },
    {
        "keywords": ["grievance", "complaint", "issue", "support ticket"],
        "answer": (
            "If you have a problem, you can submit a grievance through the MPOnline grievance process. "
            "The system will track your complaint and notify the responsible team for resolution."
        ),
        "sources": ["Manual knowledge base"],
    },
    {
        "keywords": ["documents", "upload", "knowledge base", "pdf"],
        "answer": (
            "This chatbot can use uploaded documents as a knowledge base, but it can also answer some common questions directly from built-in information. "
            "To add more content, use the manual upload API or update the built-in knowledge data in the code."
        ),
        "sources": ["Manual knowledge base"],
    },
    {
        "keywords": ["expert", "panel", "specialist", "help"],
        "answer": (
            "If the chatbot cannot answer a question, it can escalate the query to an expert panel or admin team. "
            "This helps ensure difficult questions get reviewed and answered correctly."
        ),
        "sources": ["Manual knowledge base"],
    },
    {
        "keywords": ["faq", "question", "answer", "help"],
        "answer": (
            "Ask about MPOnline services, registration, grievance handling, or how to upload documents. "
            "If your question is specific, the system will try to answer from its built-in knowledge or indexed documents."
        ),
        "sources": ["Manual knowledge base"],
    },
]


def find_manual_answer(question: str) -> dict[str, Any] | None:
    normalized = question.lower()
    for item in MANUAL_KNOWLEDGE:
        if any(keyword in normalized for keyword in item["keywords"]):
            return {
                "answer": item["answer"],
                "confidence": 0.7,
                "sources": item["sources"],
                "escalated": False,
            }
    return None
