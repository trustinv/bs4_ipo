IPO_URL = "http://www.ipostock.co.kr"

# MariaDB
DEV_DB = {
    "HOST": "ipolistingdb.civxowlytnik.ap-northeast-2.rds.amazonaws.com",
    "USER": "admin",
    "PASSWORD": "dara100400!",
    "PORT": int("3306"),
    "DB_NAME": "trustinv",
}
DB_URL = f'mariadb+pymysql://{DEV_DB["USER"]}:{DEV_DB["PASSWORD"]}@{DEV_DB["HOST"]}:{DEV_DB["PORT"]}/{DEV_DB["DB_NAME"]}'
