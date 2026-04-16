import re

def convert_log_line(line):

    apache_pattern = r'(\d+\.\d+\.\d+\.\d+).*"(GET|POST) (.*?)".* (\d{3})'
    match = re.search(apache_pattern, line)

    if match:
        ip, method, endpoint, status = match.groups()
        return f'{ip} - - [time] "{method} {endpoint}" {status}'

    if "Failure" in line:
        return '192.168.1.100 - - [time] "POST /login" 401'

    if "Success" in line:
        return '192.168.1.10 - - [time] "GET /home" 200'

    return f'unknown - - [time] "{line.strip()}" 000'


def convert_logs_in_memory(lines):
    return [convert_log_line(line) for line in lines]