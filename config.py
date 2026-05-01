from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    DB_NAME: str = "etl.db"
    DATE_KEYWORDS: dict = None
    VALID_KEYWORDS: tuple = (
        "sales",
        "failed",
        "yesterday",
        "today"
    )


CONFIG = AppConfig(
    DATE_KEYWORDS={
        "yesterday": -1,
        "today": 0
    }
)