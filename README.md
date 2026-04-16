# 🔍 NetXray — Network Log Analyzer

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Backend-black?logo=flask)
![Machine Learning](https://img.shields.io/badge/ML-IsolationForest-orange)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow?logo=javascript)
![HTML](https://img.shields.io/badge/HTML-Markup-orange?logo=html5)
![CSS](https://img.shields.io/badge/CSS-Styling-blue?logo=css3)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-green)

NetXray is a lightweight SIEM-like log analysis system that detects security threats, analyzes heterogeneous log data, and visualizes insights through an interactive dashboard.

It combines rule-based detection with machine learning and includes a log normalization layer to process different log formats into a unified structure.

---

## 🚀 Features

* 🔥 **Brute Force Detection**
  Detects repeated failed login attempts from the same IP

* 🚨 **Admin Intrusion Detection**
  Identifies unauthorized access attempts to sensitive endpoints

* 🧠 **Anomaly Detection (ML + Rules)**
  Uses Isolation Forest and rule-based logic to detect unusual patterns

* 🌍 **IP Geolocation**
  Maps IP addresses to real-world locations

* 📊 **Attack Summary Dashboard**
  Displays categorized threat counts

* 📜 **Log Timeline Visualization**
  Shows recent log activity in sequence

* 📄 **PDF Report Generation**
  Export analysis results into downloadable reports

* 🔄 **Log Normalization (NEW)**
  Converts multiple log formats (Apache, simulated system logs, etc.) into a standard format before analysis

---

## 🏗️ Project Architecture

```text
Raw Logs → Log Converter → Structured Logs → Analyzer → Dashboard
```

---

## 📁 Project Structure

```text
NetXray/
│
├── app.py  
├── analyzer.py  
├── generate_attack_logs.py  
│
├── templates/
│   └── index.html          # UI
│
├── static/
│   ├── style.css           # UI styling
│   ├── script.js           # Frontend logic
│
├── sample.log  
├── requirements.txt  
└── README.md  


 

---

## ⚙️ Installation

```bash
git clone https://github.com/Adarsh-x-0210/NetXray.git
cd NetXray
pip install -r requirements.txt
```

---

## ▶️ Usage

```bash
python app.py
```

Open in browser:

```text
http://127.0.0.1:5000
```

---

## 🧪 Log Input Options

* Upload your own log file
* Use generated logs:

```bash
python generate_attack_logs.py
```

* Use converted system logs via:

```bash
log_converter.py
```

---

## 🧠 How It Works

1. Logs are uploaded or generated
2. Log converter normalizes them into a standard format
3. Analyzer processes logs using:

   * Rule-based detection
   * Machine learning (Isolation Forest)
4. Results are displayed in a dashboard

---

## 🔒 Detection Capabilities

* Brute Force Attacks
* Admin Intrusion Attempts
* Server Errors
* Suspicious Endpoints
* Unknown Source Logs
* ML-based anomalies

---

## 🎯 Key Highlights

* Designed as a **mini SIEM system**
* Supports **heterogeneous log ingestion**
* Combines **ML + rule-based detection**
* Includes **visual dashboard + reporting**

---

## 📌 Future Improvements

* 📊 Graph-based visualization
* 🌍 Map-based IP tracking
* ⏱️ Real-time log streaming
* 🔐 User authentication system

---

## 👨‍💻 Author

**Adarsh Ajnadkar**

---

## 🌐 Live Demo

netxray.vercel.app

---

## 📜 License

MIT License
