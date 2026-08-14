from src.evaluation.ground_truth import (
    load_ground_truth,
)


def main():

    truth = load_ground_truth(
        "data/evaluation/semantic_ground_truth.csv"
    )

    print(truth)


if __name__ == "__main__":
    main()