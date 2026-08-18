from database.database import engine

try:
    with engine.connect() as connection:
        print("DATABASE CONNECTION: OK")
except Exception as e:
    print("DATABASE CONNECTION: FAILED")
    print(e)