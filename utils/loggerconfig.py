import logging


class CustomFormatter(logging.Formatter):
    # Define color codes
    grey = "\x1b[38;20m"
    cyan = "\x1b[36;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    # Define log format
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Map logging levels to color codes
    FORMATS = {
        logging.DEBUG: cyan + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Create logger
logger = logging.getLogger("llm-influencer")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels

# Create console handler and set level to DEBUG
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Add formatter to console handler
ch.setFormatter(CustomFormatter())

# Add console handler to logger
logger.addHandler(ch)
