from flask import Flask, render_template, request, jsonify, send_file
from analyzer import analyze_logs
from log_converter import convert_logs_in_memory
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

app = Flask(__name__)

# 🏠 Home
@app.route('/')
def home():
    return render_template('index.html')


# 🔍 Analyze Logs (ONLY ONE VERSION)
@app.route('/analyze', methods=['POST'])
def analyze():
    if 'logfile' not in request.files:
        return jsonify({"error": "No logfile provided"}), 400

    file = request.files['logfile']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        lines = file.read().decode().splitlines()

        # ✅ Convert logs (Vercel-safe)
        converted_logs = convert_logs_in_memory(lines)

        result = analyze_logs(converted_logs)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)}"}), 500


# 📄 Export PDF (IN-MEMORY ONLY)
@app.route('/export', methods=['POST'])
def export():
    try:
        file = request.files['logfile']
        lines = file.read().decode().splitlines()

        converted_logs = convert_logs_in_memory(lines)
        result = analyze_logs(converted_logs)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()

        content = []

        content.append(Paragraph("NetXray Log Analysis Report", styles["Title"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph(f"Total Logs: {result['total_logs']}", styles["Normal"]))
        content.append(Spacer(1, 10))

        content.append(Paragraph("Attack Summary:", styles["Heading2"]))
        for k, v in result["attack_summary"].items():
            content.append(Paragraph(f"{k}: {v}", styles["Normal"]))

        doc.build(content)
        buffer.seek(0)

        return send_file(buffer, as_attachment=True,
                         download_name="netxray_report.pdf",
                         mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500


# 🚀 Run locally
if __name__ == '__main__':
    app.run(debug=True)