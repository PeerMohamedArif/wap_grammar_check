document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("fix-form");
    const input = document.getElementById("input-text");
    const result = document.getElementById("result");
    const output = document.getElementById("output");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const text = input.value.trim();
        if (!text) return;

        output.textContent = "Processing...";
        result.style.display = "block";

        const res = await fetch("/api/fix", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ text })
        });

        const data = await res.json();
        output.textContent = data.corrected;
    });
});
