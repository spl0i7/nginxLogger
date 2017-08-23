import re
from datetime import datetime

# regex expects $remote_addr - - [$time_local] "$request" $status $bytes_sent
#   "$http_referer" "$http_user_agent"
'''
('127.0.0.1', '-', '20/Aug/2017:00:35:43 -0400', 'GET', '/', 'HTTP/', '1.1', '200', '11321', '-', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0')
'''


def get_object(line):
    regex = re.compile(
        "(?P<remote_ip>\S*)\s-\s(?P<requesting_user>\S*)\s\[(?P<timestamp>.*?)\]\s\"(?P<method>\S*)\s*(?P<request>\S*)\s*(HTTP\/)*(?P<http_version>.*?)\"\s(?P<response_code>\d{3})\s(?P<size>\S*)\s\"(?P<referrer>[^\"]*)\"\s\"(?P<client>[^\"]*)")
    r = regex.search(line)
    result_set = {
        'remote_ip': r.group('remote_ip'),
        'requesting_user': r.group('remote_ip'),
        'timestamp': datetime.strptime(r.group('timestamp'), '%d/%b/%Y:%H:%M:%S %z'),
        'method': r.group('method'),
        'request': r.group('request'),
        'http_version': r.group('http_version'),
        'response_code': r.group('response_code'),
        'size': int(r.group('size')),
        'referrer': r.group('referrer'),
        'client': r.group('client')
    }

    return result_set


def parse_access_log(seek_position, file_name):
    new_seek_pos = 0
    err_count = 0
    logs_objects = []
    with open(file_name) as f:
        f.seek(seek_position)
        lines = f.readlines()
        new_seek_pos = f.tell()
    for line in lines:
        try:
            logs_objects.append(get_object(line))
        except AttributeError:  # regex failed
            err_count += 0
    if err_count > 0:
        print('Warning : Failed to insert {} records because regex did not match'.format(err_count))
    return new_seek_pos, logs_objects
