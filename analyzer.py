import re
from collections import defaultdict
from sklearn.ensemble import IsolationForest
import requests

# 🌍 Cache to avoid repeated API calls
ip_cache = {}


# 🌍 Get IP location
def get_ip_location(ip):
    if ip in ip_cache:
        return ip_cache[ip]

    try:
        res = requests.get(f"http://ip-api.com/json/{ip}", timeout=2)
        data = res.json()
        if data["status"] == "success":
            location = f"{data['country']}, {data['city']}"
        else:
            location = "Unknown"
    except:
        location = "Unknown"

    ip_cache[ip] = location
    return location


# 🔍 Parse logs
def parse_log(line):
    pattern = r'(\d+\.\d+\.\d+\.\d+)'
    match = re.search(pattern, line)
    ip = match.group(1) if match else "unknown"

    status = "failed" if "401" in line else "success"

    return {
        "ip": ip,
        "status": status,
        "raw": line
    }


# 🔥 Brute Force Detection
def detect_bruteforce(parsed_logs):
    ip_fail_count = defaultdict(int)
    alerts = []

    for log in parsed_logs:
        if log["status"] == "failed":
            ip_fail_count[log["ip"]] += 1

    for ip, count in ip_fail_count.items():
        if count >= 5:
            alerts.append({
                "type": "Brute Force Attack",
                "ip": ip,
                "location": get_ip_location(ip),
                "risk": min(100, count * 10)
            })

    return alerts


# 🚨 Admin Intrusion Detection
def detect_admin_intrusion(parsed_logs):
    alerts = []

    for log in parsed_logs:
        if "/admin" in log["raw"] and "403" in log["raw"]:
            alerts.append({
                "type": "Admin Intrusion Attempt",
                "ip": log["ip"],
                "location": get_ip_location(log["ip"]),
                "risk": 80
            })

    return alerts


# 💥 Server Error Detection
def detect_server_errors(parsed_logs):
    errors = []

    for log in parsed_logs:
        if "500" in log["raw"]:
            errors.append({
                "type": "Server Error Spike",
                "ip": log["ip"],
                "location": get_ip_location(log["ip"]),
                "risk": 60
            })

    return errors


# 🧠 Rule-based Anomalies
def detect_anomalies(parsed_logs):
    anomalies = []

    for log in parsed_logs:

        if log["ip"] == "unknown":
            anomalies.append({
                "type": "Unknown Source",
                "ip": log["ip"],
                "location": "Unknown",
                "risk": 50
            })

        if "/config" in log["raw"]:
            anomalies.append({
                "type": "Suspicious Endpoint Access",
                "ip": log["ip"],
                "location": get_ip_location(log["ip"]),
                "risk": 70
            })

        if "500" in log["raw"]:
            anomalies.append({
                "type": "Unusual Server Error",
                "ip": log["ip"],
                "location": get_ip_location(log["ip"]),
                "risk": 60
            })

    return anomalies


# 🤖 ML Anomaly Detection
def ml_anomaly_detection(parsed_logs):
    data = []

    for log in parsed_logs:
        status = 1 if log["status"] == "failed" else 0
        is_admin = 1 if "/admin" in log["raw"] else 0
        is_error = 1 if "500" in log["raw"] else 0

        data.append([status, is_admin, is_error])

    if len(data) < 10:
        return []

    model = IsolationForest(contamination=0.2)
    preds = model.fit_predict(data)

    anomalies = []

    for i, pred in enumerate(preds):
        if pred == -1:
            anomalies.append({
                "type": "ML Detected Anomaly",
                "ip": parsed_logs[i]["ip"],
                "location": get_ip_location(parsed_logs[i]["ip"]),
                "risk": 75
            })

    return anomalies


# 📊 Attack Classification
def classify_attacks(alerts):
    summary = {}

    for alert in alerts:
        t = alert["type"]
        summary[t] = summary.get(t, 0) + 1

    return summary


# 🚀 Main Analyzer
def analyze_logs(log_lines):
    parsed = [parse_log(line) for line in log_lines]

    alerts = []
    alerts.extend(detect_bruteforce(parsed))
    alerts.extend(detect_admin_intrusion(parsed))
    alerts.extend(detect_server_errors(parsed))

    # 🧠 Rule-based anomalies
    anomalies = detect_anomalies(parsed)

    # 🤖 ML anomalies
    ml_anomalies = ml_anomaly_detection(parsed)

    anomalies.extend(ml_anomalies)

    # 📊 Summary
    attack_summary = classify_attacks(alerts)

    # 📜 Timeline (last 20 logs)
    timeline = [log["raw"] for log in parsed[-20:]]

    return {
        "total_logs": len(parsed),
        "alerts": alerts,
        "anomalies": anomalies,
        "timeline": timeline,
        "attack_summary": attack_summary
    }