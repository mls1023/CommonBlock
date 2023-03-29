import mysql.connector
import bcrypt

db = mysql.connector.connect(
    host="localhost",
    user="username",
    password="password",
    database="mydatabase"
)

cursor = db.cursor()
sql = "INSERT INTO users (username, password_hash, salt) VALUES (%s, %s, %s)"
salt = bcrypt.gensalt()
password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
cursor.execute(sql, (username, password_hash, salt))
db.commit()
cursor.close()
db.close()
