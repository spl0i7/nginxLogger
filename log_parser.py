import re
from datetime import datetime

# regex expects $remote_addr - - [$time_local] "$request" $status $bytes_sent
#   "$http_referer" "$http_user_agent"
'''
('127.0.0.1', '-', '20/Aug/2017:00:35:43 -0400', 'GET', '/', 'HTTP/', '1.1', '200', '11321', '-', 
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0')
'''


def get_object(line):
    regex = re.compile("(?P<ip_address>\S*)\s-\s(?P<requesting_user>\S*)\s\[(?P<timestamp>.*?)\]\s\"(?P<method>\S*)\s*(?P<request>\S*)\s*(HTTP\/)*(?P<http_version>.*?)\"\s(?P<response_code>\d{3})\s(?P<size>\S*)\s\"(?P<referrer>[^\"]*)\"\s\"(?P<client>[^\"]*)")
    r = regex.search(line)
    result_set = {}
    regex_group = r.groups()

    result_set['remote_ip'] = regex_group[0]
    result_set['requesting_user'] = regex_group[1]
    result_set['timestamp'] = datetime.strptime(regex_group[2], '%d/%b/%Y:%H:%M:%S %z')
    result_set['method'] = regex_group[3]
    result_set['request'] = regex_group[4]
    result_set['http_version'] = regex_group[6]
    result_set['response_code'] = regex_group[7]
    result_set['size'] = int(regex_group[8])
    result_set['referrer'] = regex_group[9]
    result_set['client'] = regex_group[10]

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
        except AttributeError:
            err_count += 0
    if err_count > 0:
        print('Warning : Failed to insert {} records because regex did not match'.format(err_count))
    return new_seek_pos, logs_objects
