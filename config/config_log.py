import os
import logging.config
from config.settings import SLACK_WEB_HOOK_URL, CONFIG_PATH


# Logging
def log_path(project_path, log_dirname="logs"):
    log_path = os.path.join(project_path, log_dirname)
    os.makedirs(log_path, exist_ok=True)
    return log_path


# log_dir_path
log_path = log_path(CONFIG_PATH)

formatter_form = {
    "format": "%(levelname)s | %(asctime)s | %(module)s | %(lineno)d | %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}
handler_form = {
    "class": "logging.handlers.RotatingFileHandler",
    "mode": "a",
    "maxBytes": 1048576,
    "backupCount": 10,
}

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": formatter_form["format"], "datefmt": "%Y-%m-%d %H:%M:%S"},
        "debug": formatter_form,
        "info": formatter_form,
        "error": formatter_form,
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "DEBUG", "formatter": "default"},
        "file_debug": {
            "level": "DEBUG",
            "formatter": "debug",
            "filename": f"{log_path}/debug.log",
            **handler_form,
        },
        "file_info": {
            "level": "INFO",
            "formatter": "info",
            "filename": f"{log_path}/info.log",
            **handler_form,
        },
        "file_error": {
            "level": "ERROR",
            "formatter": "error",
            "filename": f"{log_path}/error.log",
            **handler_form,
        },
        "slack": {
            "class": "slack_logger.SlackHandler",
            "url": SLACK_WEB_HOOK_URL,
            "level": "INFO",
            "formatter": "info",
        },
    },
    "loggers": {
        "debug-logger": {
            "level": "DEBUG",
            "handlers": ["console", "file_debug", "slack"],
            "propagate": True,
        },
        "info-logger": {
            "level": "INFO",
            "handlers": ["console", "file_info", "slack"],
            "propagate": True,
        },
        "error-logger": {
            "level": "ERROR",
            "handlers": ["console", "file_error", "slack"],
            "propagate": True,
        },
    },
}

logging.config.dictConfig(log_config)
