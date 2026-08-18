from pydantic import BaseModel


class LlmUsageMetrics(BaseModel):
    model: str

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0

    latency_seconds: float

    estimated_cost_usd: float | None = None