/*
|--------------------------------------------------------------------------
| ASP - Assets Module
|--------------------------------------------------------------------------
| assets.js
|--------------------------------------------------------------------------
*/

document.addEventListener("DOMContentLoaded", () => {

    initializeSearch();

    initializeDrawer();

});


/*==========================================================
SEARCH
==========================================================*/

function initializeSearch() {

    const input = document.getElementById("searchInput");

    if (!input) return;

    input.addEventListener("keyup", function () {

        const value = this.value.toLowerCase();

        document.querySelectorAll("#assetTable tbody tr").forEach(row => {

            row.style.display =
                row.innerText.toLowerCase().includes(value)
                    ? ""
                    : "none";

        });

    });

}


/*==========================================================
DRAWER
==========================================================*/

const drawerCache = new Map();
let currentDrawerController = null;
let lastFocusedElement = null;

function createSpinner(text) {
    const wrapper = document.createElement("div");
    wrapper.className = "d-flex align-items-center gap-2";

    const spinner = document.createElement("div");
    spinner.className = "spinner-border spinner-border-sm";
    spinner.setAttribute("role", "status");

    const label = document.createElement("span");
    label.textContent = text || "Cargando...";

    spinner.appendChild(document.createElement("span")).className = "visually-hidden";
    wrapper.appendChild(spinner);
    wrapper.appendChild(label);

    return wrapper;
}

function clearElement(element) {
    while (element && element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function initializeDrawer() {

    const backdrop = document.getElementById("drawerBackdrop");

    if (backdrop) {
        backdrop.addEventListener("click", closeDrawer);
    }

    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            closeDrawer();
        }
    });

}

async function openDrawer(assetId) {

    const drawer = document.getElementById("assetDrawer");
    const closeButton = document.getElementById("drawerCloseButton");
    const backdrop = document.getElementById("drawerBackdrop");

    if (!drawer || !closeButton || !backdrop) return;

    lastFocusedElement = document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null;

    closeDrawer({ keepFocus: true });

    drawer.setAttribute("aria-hidden", "false");
    drawer.classList.add("open");
    backdrop.classList.add("show");

    showLoading("all");

    closeButton.focus();

    try {
        const data = await getDrawerData(assetId);
        renderDrawer(data);
    } catch (error) {
        if (error.name === "AbortError") {
            console.debug("Drawer fetch aborted for assetId", assetId);
            return;
        }

        console.debug("Drawer fetch error", error);
        showError(error);
    }

}

function closeDrawer(options = {}) {

    const drawer = document.getElementById("assetDrawer");
    const backdrop = document.getElementById("drawerBackdrop");

    if (currentDrawerController) {
        currentDrawerController.abort();
        currentDrawerController = null;
    }

    if (drawer) {
        drawer.classList.remove("open");
        drawer.setAttribute("aria-hidden", "true");
    }

    if (backdrop) {
        backdrop.classList.remove("show");
    }

    if (lastFocusedElement && !options.keepFocus) {
        lastFocusedElement.focus();
        lastFocusedElement = null;
    }

}

async function getDrawerData(assetId) {

    if (drawerCache.has(assetId)) {
        console.debug("Drawer cache hit for assetId", assetId);
        return drawerCache.get(assetId);
    }

    if (currentDrawerController) {
        currentDrawerController.abort();
        currentDrawerController = null;
    }

    const controller = new AbortController();
    currentDrawerController = controller;

    const data = await fetchDrawer(assetId, controller.signal);
    drawerCache.set(assetId, data);
    return data;

}

async function fetchDrawer(assetId, signal) {

    const url = `/assets/drawer/${assetId}`;

    console.debug("Fetching drawer data", { url, assetId });

    const response = await fetch(url, {
        method: "GET",
        signal,
    });

    console.debug("Drawer response status", response.status, assetId);

    if (response.status === 200) {
        return response.json();
    }

    if (response.status === 401) {
        throw { status: 401, message: "No autorizado." };
    }

    if (response.status === 403) {
        throw { status: 403, message: "Acceso denegado." };
    }

    if (response.status === 404) {
        throw { status: 404, message: "Activo no encontrado." };
    }

    if (response.status === 500) {
        throw { status: 500, message: "Error interno del servidor." };
    }

    throw { status: response.status, message: "Error inesperado al cargar el activo." };

}

function renderDrawer(data) {

    if (!data || !data.asset) {
        showEmpty("all");
        return;
    }

    renderHeader(data.asset);
    renderOverview(data.asset);
    renderStatistics(data.stats || {});
    renderLastScan(data.last_scan || {});
    renderPorts(data.ports || []);
    renderVulnerabilities(data.vulnerabilities || []);

}

function renderHeader(asset) {

    const drawerName = document.getElementById("drawerName");
    const drawerSubtitle = document.getElementById("drawerSubtitle");
    const drawerHostname = document.getElementById("drawerHostname");
    const drawerIP = document.getElementById("drawerIPValue");
    const drawerDNS = document.getElementById("drawerDNS");
    const drawerMAC = document.getElementById("drawerMAC");
    const drawerOS = document.getElementById("drawerOS");
    const drawerType = document.getElementById("drawerType");
    const drawerCriticality = document.getElementById("drawerCriticality");
    const drawerOwner = document.getElementById("drawerOwner");
    const drawerLocation = document.getElementById("drawerLocation");

    if (drawerName) {
        drawerName.textContent = asset.name || asset.hostname || "Activo";
    }

    if (drawerSubtitle) {
        drawerSubtitle.textContent = asset.hostname || asset.ip_address || "Sin información";
    }

    if (drawerHostname) {
        drawerHostname.textContent = asset.hostname || "-";
    }

    if (drawerIP) {
        drawerIP.textContent = asset.ip_address || "-";
    }

    if (drawerDNS) {
        drawerDNS.textContent = asset.dns_name || "-";
    }

    if (drawerMAC) {
        drawerMAC.textContent = asset.mac_address || "-";
    }

    if (drawerOS) {
        drawerOS.textContent = asset.operating_system || "-";
    }

    if (drawerType) {
        drawerType.textContent = asset.asset_type || "-";
    }

    if (drawerCriticality) {
        drawerCriticality.textContent = asset.criticality || "-";
    }

    if (drawerOwner) {
        drawerOwner.textContent = asset.owner || "-";
    }

    if (drawerLocation) {
        drawerLocation.textContent = asset.location || "-";
    }

}

function renderOverview(asset) {

    const drawerOverview = document.getElementById("drawerOverview");

    if (!drawerOverview) return;

    clearElement(drawerOverview);

    const rows = [
        ["Hostname", asset.hostname || "-"],
        ["IP", asset.ip_address || "-"],
        ["Sistema", asset.operating_system || "-"],
        ["Tipo", asset.asset_type || "-"],
        ["Criticidad", asset.criticality || "-"],
    ];

    rows.forEach(([label, value]) => {
        const row = document.createElement("div");
        row.className = "mb-2";

        const strong = document.createElement("strong");
        strong.textContent = `${label}: `;

        row.appendChild(strong);
        row.appendChild(document.createTextNode(value));
        drawerOverview.appendChild(row);
    });

}

function renderStatistics(stats) {

    const totalScans = document.getElementById("drawerStatsTotalScans");
    const openPorts = document.getElementById("drawerStatsOpenPorts");
    const vulnerabilities = document.getElementById("drawerStatsVulnerabilities");
    const critical = document.getElementById("drawerStatsCritical");

    if (totalScans) {
        totalScans.textContent = stats.total_scans != null ? stats.total_scans : "-";
    }

    if (openPorts) {
        openPorts.textContent = stats.open_ports != null ? stats.open_ports : "-";
    }

    if (vulnerabilities) {
        vulnerabilities.textContent = stats.vulnerabilities != null ? stats.vulnerabilities : "-";
    }

    if (critical) {
        critical.textContent = stats.critical != null ? stats.critical : "-";
    }

}

function renderLastScan(lastScan) {

    const drawerLastScan = document.getElementById("drawerLastScan");

    if (!drawerLastScan) return;

    clearElement(drawerLastScan);

    if (!lastScan || Object.keys(lastScan).length === 0) {
        showEmpty("lastScan");
        return;
    }

    const fields = [
        ["Estado", lastScan.status || "-"],
        ["Inicio", formatDate(lastScan.started_at)],
        ["Fin", formatDate(lastScan.finished_at)],
        ["Duración", lastScan.duration != null ? `${lastScan.duration}s` : "-"],
        ["Target", lastScan.target || "-"],
    ];

    fields.forEach(([label, value]) => {
        const row = document.createElement("div");
        row.className = "mb-2";

        const strong = document.createElement("strong");
        strong.textContent = `${label}: `;

        row.appendChild(strong);
        row.appendChild(document.createTextNode(value));
        drawerLastScan.appendChild(row);
    });

}

function renderPorts(ports) {

    const drawerPorts = document.getElementById("drawerPorts");

    if (!drawerPorts) return;

    clearElement(drawerPorts);

    if (!ports || ports.length === 0) {
        showEmpty("ports");
        return;
    }

    ports.slice(0, 10).forEach((port) => {
        const item = document.createElement("div");
        item.className = "mb-2";

        const title = document.createElement("strong");
        title.textContent = `${port.port}/${port.protocol}`;

        const details = document.createElement("div");
        details.textContent = `${port.state || "-"} · ${port.service || "-"}`;

        item.appendChild(title);
        item.appendChild(details);
        drawerPorts.appendChild(item);
    });

}

function renderVulnerabilities(vulnerabilities) {

    const drawerVulns = document.getElementById("drawerVulns");

    if (!drawerVulns) return;

    clearElement(drawerVulns);

    if (!vulnerabilities || vulnerabilities.length === 0) {
        showEmpty("vulnerabilities");
        return;
    }

    vulnerabilities.slice(0, 10).forEach((vuln) => {
        const item = document.createElement("div");
        item.className = "mb-2";

        const title = document.createElement("strong");
        title.textContent = vuln.cve || "Sin CVE";

        const details = document.createElement("div");
        details.textContent = vuln.severity || "Sin severidad";

        item.appendChild(title);
        item.appendChild(details);
        drawerVulns.appendChild(item);
    });

}

function showLoading(section) {

    const drawerOverview = document.getElementById("drawerOverview");
    const drawerLastScan = document.getElementById("drawerLastScan");
    const drawerPorts = document.getElementById("drawerPorts");
    const drawerVulns = document.getElementById("drawerVulns");

    if (!section || section === "all") {
        if (drawerOverview) {
            clearElement(drawerOverview);
            drawerOverview.appendChild(createSpinner("Cargando overview..."));
        }

        if (drawerLastScan) {
            clearElement(drawerLastScan);
            drawerLastScan.appendChild(createSpinner("Cargando último scan..."));
        }

        if (drawerPorts) {
            clearElement(drawerPorts);
            drawerPorts.appendChild(createSpinner("Cargando puertos..."));
        }

        if (drawerVulns) {
            clearElement(drawerVulns);
            drawerVulns.appendChild(createSpinner("Cargando vulnerabilidades..."));
        }

        return;
    }

    if (section === "lastScan" && drawerLastScan) {
        clearElement(drawerLastScan);
        drawerLastScan.appendChild(createSpinner("Cargando último scan..."));
    }

    if (section === "ports" && drawerPorts) {
        clearElement(drawerPorts);
        drawerPorts.appendChild(createSpinner("Cargando puertos..."));
    }

    if (section === "vulnerabilities" && drawerVulns) {
        clearElement(drawerVulns);
        drawerVulns.appendChild(createSpinner("Cargando vulnerabilidades..."));
    }

}

function showEmpty(section) {

    const drawerOverview = document.getElementById("drawerOverview");
    const drawerLastScan = document.getElementById("drawerLastScan");
    const drawerPorts = document.getElementById("drawerPorts");
    const drawerVulns = document.getElementById("drawerVulns");

    if (!section || section === "all") {
        if (drawerOverview) {
            clearElement(drawerOverview);
            drawerOverview.textContent = "Sin información disponible.";
        }

        if (drawerLastScan) {
            clearElement(drawerLastScan);
            drawerLastScan.textContent = "Sin información disponible.";
        }

        if (drawerPorts) {
            clearElement(drawerPorts);
            drawerPorts.textContent = "Sin puertos registrados.";
        }

        if (drawerVulns) {
            clearElement(drawerVulns);
            drawerVulns.textContent = "Sin vulnerabilidades registradas.";
        }

        return;
    }

    if (section === "lastScan" && drawerLastScan) {
        clearElement(drawerLastScan);
        drawerLastScan.textContent = "Sin información disponible.";
    }

    if (section === "ports" && drawerPorts) {
        clearElement(drawerPorts);
        drawerPorts.textContent = "Sin puertos registrados.";
    }

    if (section === "vulnerabilities" && drawerVulns) {
        clearElement(drawerVulns);
        drawerVulns.textContent = "Sin vulnerabilidades registradas.";
    }

}

function showError(error) {

    const drawerName = document.getElementById("drawerName");
    const drawerSubtitle = document.getElementById("drawerSubtitle");
    const drawerOverview = document.getElementById("drawerOverview");
    const drawerLastScan = document.getElementById("drawerLastScan");
    const drawerPorts = document.getElementById("drawerPorts");
    const drawerVulns = document.getElementById("drawerVulns");

    const message = error && error.message ? error.message : "Error al cargar el drawer.";

    if (drawerName) {
        drawerName.textContent = "Error";
    }

    if (drawerSubtitle) {
        drawerSubtitle.textContent = message;
    }

    if (drawerOverview) {
        clearElement(drawerOverview);
        drawerOverview.textContent = message;
    }

    if (drawerLastScan) {
        clearElement(drawerLastScan);
        drawerLastScan.textContent = "No disponible.";
    }

    if (drawerPorts) {
        clearElement(drawerPorts);
        drawerPorts.textContent = "No disponible.";
    }

    if (drawerVulns) {
        clearElement(drawerVulns);
        drawerVulns.textContent = "No disponible.";
    }

}

function formatDate(date) {

    if (!date) {
        return "-";
    }

    const parsed = new Date(date);

    if (Number.isNaN(parsed.getTime())) {
        return "-";
    }

    return parsed.toLocaleString();

}

function getSeverityClass(severity) {

    if (!severity) {
        return "badge bg-secondary";
    }

    const normalized = severity.toString().toLowerCase();

    if (normalized === "critical") {
        return "badge bg-danger";
    }

    if (normalized === "high") {
        return "badge bg-warning text-dark";
    }

    if (normalized === "medium") {
        return "badge bg-info text-dark";
    }

    if (normalized === "low") {
        return "badge bg-secondary";
    }

    return "badge bg-secondary";

}


/*==========================================================
ACTIONS
==========================================================*/

function startScan() {

    alert("Escaneo disponible en el siguiente sprint.");

}


function editAsset() {

    alert("Edición disponible en el siguiente sprint.");

}


function deleteAsset() {

    if (!confirm("¿Desea eliminar este activo?")) {

        return;

    }

    alert("Eliminación disponible en el siguiente sprint.");

}


/*==========================================================
EXPORTS
==========================================================*/

window.openDrawer = openDrawer;
window.closeDrawer = closeDrawer;
window.startScan = startScan;
window.editAsset = editAsset;
window.deleteAsset = deleteAsset;
