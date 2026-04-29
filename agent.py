from datetime import date, timedelta
from difflib import get_close_matches

from app.tools import ToolRegistry
from app.config import CONFIG
from app.logger import get_logger

logger = get_logger(__name__)


class AIAgent:

    def __init__(self):
        self.registry = ToolRegistry()

    def normalize_query(self, query: str) -> str:
        words = query.lower().split()
        normalized_words = []

        for word in words:
            match = get_close_matches(
                word,
                CONFIG.VALID_KEYWORDS,
                n=1,
                cutoff=0.7
            )

            normalized_words.append(
                match[0] if match else word
            )

        return " ".join(normalized_words)

    def extract_date(self, query: str) -> str:
        today = date.today()

        for keyword, offset in (
            CONFIG.DATE_KEYWORDS.items()
        ):
            if keyword in query:
                return str(
                    today + timedelta(days=offset)
                )

        return str(today)

    def identify_intent(self, query: str):
        for keyword in self.registry.tool_map:
            if keyword in query:
                return keyword
        return None

    def respond(self, query: str):
        try:
            logger.info(
                f"Received query: {query}"
            )

            normalized_query = (
                self.normalize_query(query)
            )

            report_date = self.extract_date(
                normalized_query
            )

            intent = self.identify_intent(
                normalized_query
            )

            if not intent:
                return (
                    "Sorry, I could not "
                    "understand your request."
                )

            tool = self.registry.tool_map[intent]

            response = tool(report_date)

            logger.info(
                f"Response generated: {response}"
            )

            return response

        except Exception as ex:
            logger.exception(
                f"Agent processing failed: {ex}"
            )
            return (
                "Internal error occurred "
                "while processing request."
            )