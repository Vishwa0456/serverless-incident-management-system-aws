const API_BASE_URL = "https://8t2pmq5a6c.execute-api.ap-south-1.amazonaws.com";

function getSeverityBadgeClass(severity) {
    if (!severity) return "badge-low";
    const value = severity.toLowerCase();

    if (value === "low") return "badge badge-low";
    if (value === "medium") return "badge badge-medium";
    if (value === "high") return "badge badge-high";
    if (value === "critical") return "badge badge-critical";

    return "badge badge-low";
}
