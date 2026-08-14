from sqlalchemy import text

from src.database.session import engine


def test_connection() -> None:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        value = result.scalar_one()

        print(f"Database connection successful: {value}")


if __name__ == "__main__":
    test_connection()