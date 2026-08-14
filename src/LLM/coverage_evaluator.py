from openai import OpenAI

from src.ingestion.models import Requirement, TestCase
from src.LLM.models import CoverageAssessment


SYSTEM_INSTRUCTIONS = """
You are an AI assistant supporting validation engineers
in reviewing GxP system requirements and validation test cases.

Your job is to determine whether a supplied validation test
provides adequate evidence for a supplied user requirement.

Use the following coverage categories:

full:
The test objective, procedure, and expected result provide
clear evidence for the essential behavior required by the
requirement.

partial:
The test addresses the requirement, but important behavior,
conditions, acceptance criteria, or evidence are missing.

none:
The test does not meaningfully verify the requirement.

uncertain:
The supplied information is insufficient or ambiguous.

Rules:

1. Evaluate only the evidence provided.
2. Do not assume evidence that is not explicitly present.
3. Do not assume that a test is valid simply because it is
   semantically related to the requirement.
4. Consider the objective, test steps, and expected result.
5. Explicitly identify missing evidence.
6. Be conservative because this is a GxP validation use case.
7. Your assessment is advisory only and requires human review.
"""


def build_test_evidence(
    test_case: TestCase,
) -> str:
    """
    Convert a structured TestCase into text for LLM evaluation.

    The Related Requirements field is intentionally excluded
    so the LLM evaluates the actual test evidence rather than
    trusting the existing traceability relationship.
    """

    steps = "\n".join(
        f"{index}. {step}"
        for index, step in enumerate(
            test_case.test_steps,
            start=1,
        )
    )

    return f"""
Test ID:
{test_case.test_id}

Objective:
{test_case.objective}

Test Steps:
{steps}

Expected Result:
{test_case.expected_result}
""".strip()


class CoverageEvaluator:
    """
    Uses an LLM to assess whether one validation test
    provides adequate evidence for one requirement.
    """

    def __init__(
        self,
        model_name: str,
    ) -> None:
        self.client = OpenAI()
        self.model_name = model_name

    def evaluate(
        self,
        requirement: Requirement,
        test_case: TestCase,
    ) -> CoverageAssessment:

        test_evidence = build_test_evidence(
            test_case
        )

        user_prompt = f"""
Evaluate whether the following validation test adequately
verifies the user requirement.

USER REQUIREMENT

Requirement ID:
{requirement.requirement_id}

Requirement:
{requirement.text}


VALIDATION TEST

{test_evidence}
""".strip()

        completion = (
            self.client.chat.completions.parse(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_INSTRUCTIONS,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
                response_format=CoverageAssessment,
            )
        )

        message = completion.choices[0].message

        if message.parsed is None:
            raise RuntimeError(
                "The model did not return a valid "
                "CoverageAssessment."
            )

        return message.parsed