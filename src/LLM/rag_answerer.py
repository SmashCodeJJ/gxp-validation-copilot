from openai import OpenAI

from src.models.rag import (
    RagAnswer,
    SourceReference,
)


RAG_SYSTEM_INSTRUCTIONS = """
You are an AI assistant supporting GxP validation engineers.

Answer only from the supplied validation context.

Rules:

1. Do not invent requirements, tests, evidence, or conclusions.
2. If the context is insufficient, clearly say so.
3. Distinguish explicit traceability from semantic similarity.
4. Cite relevant requirement IDs and test IDs.
5. Do not claim a requirement is validated only because a
   semantically similar test exists.
6. Final validation decisions require human review.
"""


def build_rag_context(
    documents,
) -> str:
    sections = []

    for document in documents:
        sections.append(
            f"""
SOURCE TYPE: {document.source_type}
SOURCE ID: {document.source_id}
SOURCE DOCUMENT: {document.source_document}

CONTENT:
{document.text}
""".strip()
        )

    return "\n\n---\n\n".join(sections)


class RagAnswerer:

    def __init__(
        self,
        model_name: str,
    ) -> None:
        self.client = OpenAI()
        self.model_name = model_name

    def answer(
        self,
        question: str,
        documents,
    ) -> RagAnswer:

        context = build_rag_context(documents)

        prompt = f"""
QUESTION:

{question}


VALIDATION CONTEXT:

{context}
""".strip()

        response = self.client.responses.parse(
            model=self.model_name,
            instructions=RAG_SYSTEM_INSTRUCTIONS,
            input=prompt,
            text_format=RagAnswer,
        )

        return response.output_parsed