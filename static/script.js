"use strict";
var _a, _b, _c;
(_a = document.getElementById("export-btn")) === null || _a === void 0 ? void 0 : _a.addEventListener("click", () => {
    fetch("/dataset").then(res => {
        if (res.ok)
            alert("Exported");
    });
});
(_b = document.getElementById("label-btn")) === null || _b === void 0 ? void 0 : _b.addEventListener("click", () => {
    const form = document.getElementById("form");
    if (form) {
        const data = [];
        new FormData(form).forEach((v, k) => {
            data.push({ seq: parseInt(k), label: parseInt(v) });
        });
        fetch("/label", { body: JSON.stringify(data), headers: { "Content-Type": "application/json" }, method: "PATCH" }).then(res => {
            if (res.ok)
                window.location.reload();
        });
    }
});
(_c = document.getElementById("scan-btn")) === null || _c === void 0 ? void 0 : _c.addEventListener("click", () => {
    window.location.href = "/";
});
