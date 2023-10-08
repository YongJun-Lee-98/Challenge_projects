import pymysql
import json

with open('config.json') as f:
    config = json.load(f)

host_name = config["host"]
user_name = config["user"]
password = config["password"]
database_name = config["database"]

db = None

try:
    db = pymysql.connect(
        host=host_name,
        user=user_name,
        password=password,
        db=database_name
    )

    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 마지막에는 반드시 연결을 닫습니다.
    # 이때, db가 None이 아닌 경우만 close를 호출하도록 합니다.
    if db is not None:
        db.close()
