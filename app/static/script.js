const attackCanvas = document.getElementById("attackChart");

if (attackCanvas) {
    const counts = JSON.parse(attackCanvas.dataset.attackCounts || "[0, 0, 0]");

    new Chart(attackCanvas, {
        type: "bar",
        data: {
            labels: ["Brute Force", "SQLi", "XSS"],
            datasets: [
                {
                    label: "Attack Count",
                    data: counts,
                    backgroundColor: ["#ef4444", "#f59e0b", "#22c55e"],
                    borderColor: ["#b91c1c", "#92400e", "#166534"],
                    borderWidth: 1,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        color: "#cbd5e1",
                    },
                },
                x: {
                    ticks: {
                        color: "#cbd5e1",
                    },
                },
            },
            plugins: {
                legend: {
                    labels: {
                        color: "#e2e8f0",
                    },
                },
            },
        },
    });
}
