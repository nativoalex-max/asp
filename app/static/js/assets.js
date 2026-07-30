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


function openDrawer(asset) {

    const drawer = document.getElementById("assetDrawer");

    if (!drawer) return;

    document.getElementById("drawerName").textContent =
        asset.name || "-";

    document.getElementById("drawerHostname").textContent =
        asset.hostname || "-";

    document.getElementById("drawerIP").textContent =
        asset.ip || "-";

    document.getElementById("drawerDNS").textContent =
        asset.dns || "-";

    document.getElementById("drawerMAC").textContent =
        asset.mac || "-";

    document.getElementById("drawerOS").textContent =
        asset.os || "-";

    document.getElementById("drawerType").textContent =
        asset.type || "-";

    document.getElementById("drawerCriticality").textContent =
        asset.criticality || "-";

    document.getElementById("drawerOwner").textContent =
        asset.owner || "-";

    document.getElementById("drawerLocation").textContent =
        asset.location || "-";

    drawer.classList.add("open");

    document
        .getElementById("drawerBackdrop")
        .classList.add("show");

}


function closeDrawer() {

    const drawer = document.getElementById("assetDrawer");

    if (drawer) {

        drawer.classList.remove("open");

    }

    const backdrop = document.getElementById("drawerBackdrop");

    if (backdrop) {

        backdrop.classList.remove("show");

    }

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


// TODO Fase 2: reemplazar openDrawer por versión AJAX.
