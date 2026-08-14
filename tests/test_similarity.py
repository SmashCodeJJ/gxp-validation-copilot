import pytest

from src.semantic.similarity import cosine_similarity


def test_identical_normalized_vectors():
    score = cosine_similarity(
        [1.0, 0.0],
        [1.0, 0.0],
    )

    assert score == pytest.approx(1.0)


def test_orthogonal_vectors():
    score = cosine_similarity(
        [1.0, 0.0],
        [0.0, 1.0],
    )

    assert score == pytest.approx(0.0)


def test_dimension_mismatch():
    with pytest.raises(
        ValueError,
        match="same dimensions",
    ):
        cosine_similarity(
            [1.0, 0.0],
            [1.0],
        )