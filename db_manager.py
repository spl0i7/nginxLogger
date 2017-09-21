from pymongo import MongoClient
import bcrypt

connection = MongoClient()
db = connection.nginxLogger


def insert_user(username, password):
    if username is not None and password is not None:
        secret = bcrypt.hashpw(password, bcrypt.gensalt(10))
        db.user.insert({'username': username, 'secret': secret}, w=0)

def insert_record(record):
    if len(record) > 0 or record is not None:
        db.access_logs.insert(record, w=0)


def insert_position(position):
    db.file_position.update({}, {'$set': {'position': position}}, upsert=True)


def get_position():
    record = db.file_position.find_one()
    if not record:
        return 0
    else:
        return record['position']
