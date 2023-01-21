import os
from collections import namedtuple

from pydantic import BaseSettings


import os
import pathlib
from functools import lru_cache


def get_path(arg=None):
    if arg is not None:
        path = arg
    else:
        path = os.getcwd()
    path = os.path.abspath(path)
    return path


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/db.sqlite3")
    DATABASE_CONNECT_DICT: dict = {}
    settings_path = get_path(__file__)
    config_path = os.path.dirname(settings_path)
    project_path = os.path.dirname(config_path)


class DevelopmentConfig(BaseConfig):
    IPO_URL = "http://www.ipostock.co.kr"

    HOST: str = "ipolistingdb.civxowlytnik.ap-northeast-2.rds.amazonaws.com"
    USER: str = "admin"
    PASSWORD: str = "dara100400!"
    PORT: str = 3306
    DB_NAME: str = "test_trustinv"

    DB_URL = f"mariadb+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    ASYNC_DB_URL = f"mysql+aiomysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    DELISTING = "공모철회"


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }

    config_name = os.environ.get("BS4_IPO_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
