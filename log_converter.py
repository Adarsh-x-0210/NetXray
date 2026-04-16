import re

def convert_log_line(line):

    # 🔹 Apache/Nginx logs
    apache_pattern = r'(\d+\.\d+\.\d+\.\d+).*"(GET|POST) (.*?)".* (\d{3})'
    match = re.search(apache_pattern, line)
    if match:
        ip, method, endpoint, status = match.groups()
        return f'{ip} - - [time] "{method} {endpoint}" {status}'

    # 🔹 Windows log simulation
    if "Failure" in line:
        return '192.168.1.100 - - [time] "POST /login" 401'

    if "Success" in line:
        return '192.168.1.10 - - [time] "GET /home" 200'

    # 🔹 Unknown fallback
    return f'unknown - - [time] "{line.strip()}" 000'


def convert_logs(input_file, output_file="sample.log"):
    with open(input_file, "r", errors="ignore") as f:
        lines = f.readlines()

    converted = []

    for line in lines:
        new_line = convert_log_line(line)
        converted.append(new_line)

    with open(output_file, "w") as f:
        f.write("\n".join(converted))

    print("Logs converted successfully!")