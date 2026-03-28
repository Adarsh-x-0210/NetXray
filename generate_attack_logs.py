import random
from datetime import datetime, timedelta
import os

normal_ips = ["192.168.1.10", "192.168.1.20", "10.0.0.5"]
attacker_ips = ["185.243.115.84", "45.67.89.10", "103.56.22.1"]

paths = ["/home", "/dashboard", "/profile", "/login"]
admin_paths = ["/admin", "/admin/login", "/config"]

status_codes = [200, 200, 200, 404]

MAX_LINES = 300


# ✅ Count lines in file
def get_line_count(filename):
    if not os.path.exists(filename):
        return 0
    with open(filename, "r") as f:
        return len(f.readlines())


# ✅ Get last timestamp for continuity
def get_last_timestamp(filename):
    if not os.path.exists(filename):
        return datetime.now()

    with open(filename, "r") as f:
        lines = f.readlines()
        if not lines:
            return datetime.now()

        last_line = lines[-1]
        try:
            time_str = last_line.split("[")[1].split("]")[0]
            return datetime.strptime(time_str, "%d/%b %H:%M:%S")
        except:
            return datetime.now()


def format_time(dt):
    return dt.strftime("%d/%b %H:%M:%S")


def generate_logs(filename="sample.log"):
    line_count = get_line_count(filename)

    # 🔥 Decide mode
    mode = "w" if line_count >= MAX_LINES else "a"

    if mode == "w":
        print("[!] Log file exceeded 300 lines → resetting file")

    current_time = datetime.now() if mode == "w" else get_last_timestamp(filename)

    with open(filename, mode) as f:

        # Normal traffic
        for _ in range(30):
            ip = random.choice(normal_ips)
            path = random.choice(paths)
            status = random.choice(status_codes)
            current_time += timedelta(seconds=1)
            f.write(f'{ip} - - [{format_time(current_time)}] "GET {path}" {status}\n')

        # Brute force attack
        attacker = random.choice(attacker_ips)
        for _ in range(10):
            current_time += timedelta(seconds=1)
            f.write(f'{attacker} - - [{format_time(current_time)}] "POST /login" 401\n')

        current_time += timedelta(seconds=1)
        f.write(f'{attacker} - - [{format_time(current_time)}] "POST /login" 200\n')

        # Admin intrusion
        attacker2 = random.choice(attacker_ips)
        for _ in range(5):
            path = random.choice(admin_paths)
            current_time += timedelta(seconds=1)
            f.write(f'{attacker2} - - [{format_time(current_time)}] "GET {path}" 403\n')

        # Server errors
        for _ in range(5):
            ip = random.choice(normal_ips)
            current_time += timedelta(seconds=1)
            f.write(f'{ip} - - [{format_time(current_time)}] "GET /dashboard" 500\n')

    print(f"[+] Logs written in '{filename}' (mode: {'overwrite' if mode=='w' else 'append'})")


if __name__ == "__main__":
    generate_logs()