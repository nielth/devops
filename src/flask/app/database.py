import os
import pymysql
import hashlib
import datetime

user_db_file_location = "database_file/users.db"
note_db_file_location = "database_file/notes.db"
image_db_file_location = "database_file/images.db"

from dotenv import load_dotenv

load_dotenv()
MYSQL_ROOT_USER = os.getenv("MYSQL_ROOT_USER")
MYSQL_ROOT_PASSWORD = os.getenv("MYSQL_ROOT_PASSWORD")
MYSQL_IP = os.getenv("MYSQL_IP")

def list_users():
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    _c.execute("SELECT id FROM users;")
    result = [x['id'] for x in _c.fetchall()]

    _conn.close()
    
    return result

def verify(id, pw):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    _c.execute("SELECT pw FROM users WHERE id = '" + id + "';")
    result = _c.fetchone()['pw'] == hashlib.sha256(pw.encode()).hexdigest()
    
    _conn.close()

    return result

def delete_user_from_db(id):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()
    _c.execute("DELETE FROM users WHERE id = '" + id + "';")
    _conn.commit()
    _conn.close()

    # when we delete a user FROM database USERS, we also need to delete all his or her notes data FROM database NOTES
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()
    _c.execute("DELETE FROM notes WHERE user = '" + id + "';")
    _conn.commit()
    _conn.close()

    # when we delete a user FROM database USERS, we also need to 
    # [1] delete all his or her images FROM image pool (done in app.py)
    # [2] delete all his or her images records FROM database IMAGES
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()
    _c.execute("DELETE FROM images WHERE owner = '" + id + "';")
    _conn.commit()
    _conn.close()

def add_user(id, pw):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    _c.execute("INSERT INTO users VALUES(%s, %s)", (id.upper(), hashlib.sha256(pw.encode()).hexdigest()))
    
    _conn.commit()
    _conn.close()

def read_note_from_db(id):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    command = "SELECT note_id, timestamp, note FROM notes WHERE user = '" + id.upper() + "';" 
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result

def match_user_id_with_note_id(note_id):
    # Given the note id, confirm if the current user is the owner of the note which is being operated.
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    command = "SELECT user FROM notes WHERE note_id = '" + note_id + "';" 
    _c.execute(command)
    result = _c.fetchone()['user']

    _conn.commit()
    _conn.close()

    return result

def write_note_into_db(id, note_to_write):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    current_timestamp = str(datetime.datetime.now())
    _c.execute("INSERT INTO notes values(%s, %s, %s, %s)", (id.upper(), current_timestamp, note_to_write, hashlib.sha1((id.upper() + current_timestamp).encode()).hexdigest()))

    _conn.commit()
    _conn.close()

def delete_note_from_db(note_id):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    command = "DELETE FROM notes WHERE note_id = '" + note_id + "';" 
    _c.execute(command)

    _conn.commit()
    _conn.close()

def image_upload_record(uid, owner, image_name, timestamp):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    _c.execute("INSERT INTO images VALUES (%s, %s, %s, %s)", (uid, owner, image_name, timestamp))

    _conn.commit()
    _conn.close()

def list_images_for_user(owner):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    command = "SELECT uid, timestamp, name FROM images WHERE owner = '{0}'".format(owner)
    _c.execute(command)
    result = _c.fetchall()

    _conn.commit()
    _conn.close()

    return result

def match_user_id_with_image_uid(image_uid):
    # Given the note id, confirm if the current user is the owner of the note which is being operated.
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    command = "SELECT owner FROM images WHERE uid = '" + image_uid + "';" 
    _c.execute(command)
    result = _c.fetchone()['owner']

    _conn.commit()
    _conn.close()

    return result

def delete_image_from_db(image_uid):
    _conn = pymysql.connect(host=MYSQL_IP,
                             user=MYSQL_ROOT_USER,
                             password=MYSQL_ROOT_PASSWORD,
                             database='db',
                             cursorclass=pymysql.cursors.DictCursor)
    _c = _conn.cursor()

    command = "DELETE FROM images WHERE uid = '" + image_uid + "';" 
    _c.execute(command)

    _conn.commit()
    _conn.close()







if __name__ == "__main__":
    print(list_users())
