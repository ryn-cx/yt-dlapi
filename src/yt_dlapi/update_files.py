import logging
from pathlib import Path

from gapix import GAPIX

from yt_dlapi.constants import JUST_SCRAPE_DIR, TEST_FILE_DIR

logger = logging.getLogger(__name__)


class Updater(GAPIX):
    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    def output_file(self) -> Path:
        return JUST_SCRAPE_DIR / f"{self.endpoint}/models.py"

    def input_folder(self) -> Path:
        return TEST_FILE_DIR / self.endpoint

    def class_name(self) -> str:
        return self.endpoint.replace("_", " ").title().replace(" ", "")


def update_all_schemas() -> None:
    for endpoint in TEST_FILE_DIR.glob("*"):
        if endpoint.is_dir():
            logger.info("Updating schema for %s", endpoint.name)
            updater = Updater(endpoint.name)
            updater.generate_schema()
            updater.remove_redundant_files()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    update_all_schemas()
