import os
import pymysql
from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI + MySQL"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/items")
def get_items():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM items;")
            result = cursor.fetchall()
            return result
    finally:
        connection.close()

@app.post("/items/{name}")
def create_item(name: str):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO items (name) VALUES (%s);", (name,))
            connection.commit()
            return {"message": "Item added successfully", "name": name}
    finally:
        connection.close()

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            affected_rows = cursor.execute("DELETE FROM items WHERE id = %s;", (item_id,))
            connection.commit()
            if affected_rows == 0:
                raise HTTPException(status_code=404, detail="Item not found")
            return {"message": "Item deleted successfully", "id": item_id}
    finally:
        connection.close()
        
