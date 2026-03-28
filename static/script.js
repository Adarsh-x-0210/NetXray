let hasUploaded = false;

function uploadLog() {
    const fileInput = document.getElementById("logfile");
    const file = fileInput.files[0];

    if (!file) return;

    // 🔥 SHOW LOADER
    document.getElementById("loaderOverlay").style.display = "flex";

    const formData = new FormData();
    formData.append("logfile", file);

    fetch("/analyze", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        updateUI(data);

        // ✅ HIDE LOADER
        document.getElementById("loaderOverlay").style.display = "none";
    })
    .catch(() => {
        document.getElementById("loaderOverlay").style.display = "none";
    });
}


// 🔥 Auto refresh ONLY after upload
setInterval(() => {
    if (!hasUploaded) return;

    fetch("/auto_analyze")
    .then(res => res.json())
    .then(updateUI);
}, 5000);


function updateUI(data) {
    if (!data || data.error) return;

    document.getElementById("totalLogs").innerText = data.total_logs;
    document.getElementById("alertsCount").innerText = data.alerts.length;
    document.getElementById("anomalyCount").innerText = data.anomalies.length;
    document.getElementById("attackSummaryBox").style.display = "block";
    document.getElementById("exportSection").style.display = "block";

    // Alerts
    const alertsList = document.getElementById("alertsList");
    alertsList.innerHTML = "";
    data.alerts.forEach(a => {
        const li = document.createElement("li");

        let color = "white";
        if (a.risk >= 80) color = "red";
        else if (a.risk >= 60) color = "orange";
        else color = "yellow";

        li.style.color = color;
        li.innerText = `${a.type} | IP: ${a.ip} | Risk: ${a.risk}`;
        alertsList.appendChild(li);
    });

    // Anomalies
    const anomalyList = document.getElementById("anomalyList");
    anomalyList.innerHTML = "";
    data.anomalies.forEach(a => {
        const li = document.createElement("li");
        li.innerText = `${a.type} | Risk: ${a.risk}`;
        anomalyList.appendChild(li);
    });

    // Timeline
    document.getElementById("timeline").innerText =
        data.timeline.join("\n");
    
        // Attack Summary
const summaryList = document.getElementById("attackSummary");
summaryList.innerHTML = "";

if (data.attack_summary) {
    for (let key in data.attack_summary) {
        const li = document.createElement("li");
        li.innerText = `${key}: ${data.attack_summary[key]}`;
        summaryList.appendChild(li);
    }
}
}
function showFileName() {
    const fileInput = document.getElementById("logfile");

    if (fileInput.files.length > 0) {
        document.getElementById("fileName").innerText =
            fileInput.files[0].name;
    } else {
        document.getElementById("fileName").innerText =
            "No file selected";
    }
}
function downloadReport() {
    window.location.href = "/export";
}
