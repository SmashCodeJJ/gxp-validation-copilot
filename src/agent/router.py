from openai import OpenAI

from src.agent.models import (
    AgentDecision,
)


ROUTER_INSTRUCTIONS = """
You are a routing component for a GxP validation assistant.

Choose exactly one tool.

Available tools:

traceability:
Use for deterministic questions about explicit requirement-to-test
relationships, missing test coverage, or traced/untraced requirements.

semantic_search:
Use when the user wants semantically similar requirements or tests.

coverage_analysis:
Use when the user asks whether a test adequately verifies a requirement,
or asks for AI-assisted coverage analysis for a specific requirement.

rag:
Use for broader questions requiring explanation or retrieval from validation
documents.

Rules:

1. Prefer deterministic tools over RAG when the question can be answered
   deterministically.
2. Do not invent requirement IDs or test IDs.
3. Extract identifiers when explicitly present in the user question.
"""


class AgentRouter:

    def __init__(
        self,
        model_name: str,
        api_key: str,
    ) -> None:
        self.client = OpenAI(
            api_key = api_key
        )
        self.model_name = model_name

    def route(
        self,
        question: str,
    ) -> AgentDecision:

        response = self.client.responses.parse(
            model=self.model_name,
            instructions=ROUTER_INSTRUCTIONS,
            input=question,
            text_format=AgentDecision,
        )

        return response.output_parsed
