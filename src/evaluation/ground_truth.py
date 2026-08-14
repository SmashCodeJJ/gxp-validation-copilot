import csv
from pathlib import Path


def load_ground_truth(
    path: str,
) -> dict[str, str]:

    ground_truth = {}

    with open(
        Path(path),
        newline="",
        encoding="utf-8",
    ) as csv_file:

        reader = csv.DictReader(csv_file)

        for row in reader:

            ground_truth[
                row["requirement_id"]
            ] = row["expected_test_id"]

    return ground_truth