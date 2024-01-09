import logging
import logging.config  # noqa


def set_logger(log_level: str) -> None:
    """Airbrakeとloggingの統合"""
    match log_level.lower():
        case "debug":
            level = logging.DEBUG
        case "info":
            level = logging.INFO
        case "warning":
            level = logging.WARNING
        case "error":
            level = logging.ERROR
        case "critical":
            level = logging.CRITICAL

    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "raw": {
                "format": "%(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "raw",
                "level": level,
            },
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": level,
            },
        },
    }

    logging.config.dictConfig(LOGGING_CONFIG)
