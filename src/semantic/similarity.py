def cosine_similarity(
    first: list[float],
    second: list[float],
) -> float:
    """
    Calculate cosine similarity between two normalized vectors.
    """

    if len(first) != len(second):
        raise ValueError(
            "Embeddings must have the same dimensions."
        )

    if not first:
        raise ValueError("Embeddings cannot be empty.")

    return sum(
        first_value * second_value
        for first_value, second_value in zip(
            first,
            second,
        )
    )