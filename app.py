from generate_attack_logs import generate_logs
import json
import os
from flask import Flask, render_template, request, jsonify,send_file
from analyzer import analyze_logs
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

@app.route('/export')
def export():
    try:
        with open("sample.log", "r") as f:
            logs = f.read().splitlines()

        result = analyze_logs(logs)

        from io import BytesIO
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = []

        # Title
        content.append(Paragraph("NetXray Log Analysis Report", styles["Title"]))
        content.append(Spacer(1, 10))

        # Summary
        content.append(Paragraph(f"Total Logs: {result['total_logs']}", styles["Normal"]))
        content.append(Spacer(1, 10))

        # Attack Summary
        content.append(Paragraph("Attack Summary:", styles["Heading2"]))
        for k, v in result["attack_summary"].items():
            content.append(Paragraph(f"{k}: {v}", styles["Normal"]))
        content.append(Spacer(1, 10))

        # Alerts
        content.append(Paragraph("Alerts:", styles["Heading2"]))
        for a in result["alerts"]:
            content.append(Paragraph(
                f"{a['type']} | IP: {a['ip']} ({a['location']}) | Risk: {a['risk']}",
                styles["Normal"]
            ))
        content.append(Spacer(1, 10))

        # Anomalies
        content.append(Paragraph("Anomalies:", styles["Heading2"]))
        for a in result["anomalies"]:
            content.append(Paragraph(
                f"{a['type']} | IP: {a['ip']} | Risk: {a['risk']}",
                styles["Normal"]
            ))

        doc.build(content)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="netxray_report.pdf", mimetype="application/pdf")
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'logfile' not in request.files:
        return jsonify({"error": "No logfile provided"}), 400
    
    file = request.files['logfile']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    try:
        logs = file.read().decode('utf-8').splitlines()
        result = analyze_logs(logs)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500

@app.route('/auto_analyze')
def auto_analyze():
    try:
        # 🔥 generate new logs every refresh
        generate_logs()

        if not os.path.exists("sample.log"):
            return jsonify({"error": "No sample.log generated"}), 404

        with open("sample.log", "r") as f:
            logs = f.read().splitlines()

        return jsonify(analyze_logs(logs))
    except Exception as e:
        return jsonify({"error": f"Auto-analysis failed: {str(e)}"}), 500
if __name__ == '__main__':
    app.run(debug=True)