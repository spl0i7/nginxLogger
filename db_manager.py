from pymongo import MongoClient

connection = MongoClient()
db = connection.nginxLogger


def insert_record(objects):
    db.access_logs.insert(objects, w=0)


def insert_position(position):
    db.file_position.update({}, {'$set': {'position': position}}, upsert=True)


def get_position():
    record = db.file_position.find_one()
    if not record:
        return 0
    else:
        return record['position']
