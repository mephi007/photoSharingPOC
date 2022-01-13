# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import psycopg2
from flask import Flask

app = Flask(__name__)

conn = None


def db_connection():
    global conn
    if conn is None or conn.closed:
        conn = psycopg2.connect("dbname=postgres user=sumitroy password=admin")
    return conn


@app.before_first_request
def connect_to_db():
    try:
        db_connection()
        cur = conn.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        create_table_query = '''
                    CREATE TABLE IF NOT EXISTS images
                    (
                     img_id SERIAL PRIMARY KEY,
                     img_caption TEXT,
                     image BYTEA
                     );
                    '''
        cur.execute(create_table_query)
        conn.commit()
        print("Table images created")
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


@app.route("/")
def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    return "hello world"  # Press ⌘F8 to toggle the breakpoint.


@app.route("/add_image")
def add_images():
    img_caption = "Inserting image"
    image = "Images/Naruto1.jpeg"
    db_connection()
    cur = conn.cursor()
    insert_query = '''
        INSERT INTO images (img_caption, image) values(%s, bytea(%s));
    '''
    values = [img_caption, image]
    cur.execute(insert_query, values)
    conn.commit()
    return '{} inserted'.format(img_caption)


@app.route("/update_image_detail")
def update_image_details():
    img_caption = "Inserting Naruto Image"
    img_id = 1
    db_connection()
    cur = conn.cursor()
    update_query = '''
        UPDATE images SET img_caption=%s WHERE img_id=%s;
    '''
    values = [img_caption, img_id]
    cur.execute(update_query, values)
    conn.commit()
    return '{} updated with {}'.format(img_id, img_caption)


@app.route("/delete_image")
def delete_image():
    img_id = 2
    db_connection()
    cur = conn.cursor()
    delete_query = '''
        DELETE FROM images where img_id=%s;
    '''
    values = [img_id]
    cur.execute(delete_query, values)
    conn.commit()
    return '{} deleted'.format(img_id)


if __name__ == '__main__':
    app.run(debug=True)
