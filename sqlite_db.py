import sqlite3


async def create_customers_db():
    global DB_NAME
    DB_NAME = "person_db.db"

    with sqlite3.connect(DB_NAME) as sqlite_conn:
        sql_request = """CREATE TABLE IF NOT EXISTS customers (
            id integer PRIMARY KEY,
            name text,
            phone_num text
        );"""
        sqlite_conn.execute(sql_request)


async def create_profile(user_id):
    with sqlite3.connect(DB_NAME) as sqlite_conn:
        sql_request = f"SELECT 1 FROM customers WHERE id == '{user_id}'"
        user = sqlite_conn.execute(sql_request).fetchone()
        if not user:
            sql_request = "INSERT INTO customers VALUES(?, ?, ?)"
            sqlite_conn.execute(sql_request, (user_id, '', ''))
            sqlite_conn.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        with sqlite3.connect(DB_NAME) as sqlite_conn:
            sql_request = f"UPDATE customers SET name = '{data['name']}', phone_num = '{data['phone']}' WHERE id == '{user_id}'"
            sqlite_conn.execute(sql_request)
            sqlite_conn.commit()


