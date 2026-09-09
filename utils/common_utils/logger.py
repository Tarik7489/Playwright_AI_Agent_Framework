import logging


class LoggerReports:
    def __init__(self) -> None:
        self.logger = logging.getLogger("automation")
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
            self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def step(self, message: str) -> None:
        self.logger.info(message)
