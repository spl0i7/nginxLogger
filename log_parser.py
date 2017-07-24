import re
from bson.objectid import ObjectId
from datetime import datetime

# regex expects $remote_addr - - [$time_local] "$request" $status $bytes_sent
#   "$http_referer" "$http_user_agent"
regex = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*)\] \"(\w{3,6}) (.*) \w{0,4}/\d\.\d\" (\d+) (\d+) "(\S+)" "(.*)"')


def get_object(log_list):
    return {
        '_id': ObjectId(),
        'remote_ip': log_list[0],
        'time': datetime.strptime(log_list[1], '%d/%b/%Y:%H:%M:%S %z'),
        'request_type': log_list[2],
        'path': log_list[3],
        'status_code': log_list[4],
        'bytes_sent': log_list[5],
        'referer': log_list[6],
        'user_agent': log_list[7]
    }


def parse_access_log(seek_position, file_name):
    new_seek_pos = 0
    logs_objects = []
    with open(file_name) as f:
        f.seek(seek_position)
        lines = f.readlines()
        new_seek_pos = f.tell()
    for line in lines:
        r = regex.search(line)
        logs_objects.append(get_object(r.groups()))
    return new_seek_pos, logs_objects
