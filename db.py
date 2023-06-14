import os
import psycopg2

def get_connection():
    url = os.environ['DATABASE_URL']
    connection = psycopg2.connect(url)
    
    return connection

def select_all_books():
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM books'
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    connection.close()
    cursor.close()
    
    return rows



def insert_book(title, author, publisher, isbn, category):
    connection = get_connection()
    cursor = connection.cursor()
    
    sql = 'INSERT INTO books_sample VALUES (default , %s,%s,%s,%s,%s)'
    cursor.close()
    connection.close()
    
def select_title_books(title):
    connection = get_connection()
    cursor = connection.cursor()
    sql = 'SELECT * FROM books_sample WHERE title LIKE ?'
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows



