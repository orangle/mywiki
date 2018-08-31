import re 
import time 
import sys

log_re_str = ('^(?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|-) .* '
             '\[(?P<time_local>.*?)\] '
             '"(?P<request>.*?)" '
             '(?P<status>[^ ]*) '
             '(?P<request_time>[^ ]*) '
             '(?P<body_bytes_sent>[^ ]*) '
             '(?P<bytes_sent>[^ ]*) '
             '"(?P<http_referer>[^"]*)" '
             '"(?P<http_user_agent>[^"]*)" '
             '"(?P<http_x_forwarded_for>[^"]*)" '
             '(?P<connection>[^ ]*) '
             '"(?P<hit>[^"]*)" '
             '"(?P<server_addr>[^"]*)" ' 
             '(?P<cdn>.*)')

log_re = re.compile(log_re_str)

def split_parse(line):
    tmp = line.split('"')
    if len(tmp) == 15:
        hit = tmp[11]
        sip = tmp[13]
    elif len(tmp) == 13:
        hit = tmp[10].strip()
        sip = '-'

    ip_time = tmp[0]
    request = tmp[1]
    code_bytes = tmp[2]

    cip, _, _, time_str, _ = ip_time.split()
    dtime = time_str[1:]
    status, cost, _, send_bytes = code_bytes.split()

    res = {
        'cip': cip,
        'dtime': dtime,
        'request': request,
        'status': status,
        'cost': cost,
        'bytes': send_bytes,
        'hit': hit,
        'sip': sip
    }


def regex_v1(lines):
    for msg in lines:
        res = re.search(log_re, msg)


def split_v1(lines):
    for msg in lines:
        try:
            split_parse(msg)
        except Exception as e:
            print(msg)
            print(e)
            sys.exit(1)


def test():
    log_lines = []
    with open("log.txt") as f:
        for line in f:
            log_lines.append(line.strip()) 

    print("lines nums {}".format(len(log_lines)))
    start = time.time()
    repeat = 2000

    for i in range(repeat):
        # regex_v1(log_lines)
        split_v1(log_lines)

    total = len(log_lines) * repeat
    total_time = time.time() - start
    print("rps is {}/s".format(int(total/total_time)))


if __name__ == "__main__":
    test()
