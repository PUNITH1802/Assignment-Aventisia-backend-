import logging
import sys


def setup_logging(debug: bool = False) -> None:
    """Configure application-wide logging."""
    level = logging.DEBUG if debug else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)-8s | %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    uvicorn_loggers = ["uvicorn", "uvicorn.access", "uvicorn.error"]
    for name in uvicorn_loggers:
        logging.getLogger(name).setLevel(level)
