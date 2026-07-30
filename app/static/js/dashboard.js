async function loadDashboard() {

    try {

        const response = await fetch("/api/dashboard/summary");

        const data = await response.json();

        document.getElementById("assets").textContent = data.assets;
        document.getElementById("scans").textContent = data.scans;
        document.getElementById("vulns").textContent = data.vulnerabilities;
        document.getElementById("risk").textContent = data.risk_score + "%";

        document.getElementById("platformStatus").textContent =
            data.platform_status;

        document.getElementById("lastScan").textContent =
            data.last_scan || "Sin escaneos";

        document.getElementById("critical").textContent =
            data.severity.CRITICAL;

        document.getElementById("high").textContent =
            data.severity.HIGH;

        document.getElementById("medium").textContent =
            data.severity.MEDIUM;

        document.getElementById("low").textContent =
            data.severity.LOW;

        loadPorts(data.top_ports);

        loadProducts(data.top_products);

        const bar = document.getElementById("riskBar");

        bar.style.width = data.risk_score + "%";

        if (data.risk_score >= 75)
            bar.className = "progress-bar bg-danger";

        else if (data.risk_score >= 50)
            bar.className = "progress-bar bg-warning";

        else
            bar.className = "progress-bar bg-success";

    } catch (e) {

        console.error(e);

    }

}

function loadPorts(list) {

    const body = document.getElementById("ports");

    body.innerHTML = "";

    list.forEach(item => {

        body.innerHTML += `
            <tr>
                <td>${item.port}</td>
                <td>${item.count}</td>
            </tr>
        `;

    });

}

function loadProducts(list) {

    const body = document.getElementById("products");

    body.innerHTML = "";

    list.forEach(item => {

        body.innerHTML += `
            <tr>
                <td>${item.product}</td>
                <td>${item.count}</td>
            </tr>
        `;

    });

}

loadDashboard();

setInterval(loadDashboard,10000);
