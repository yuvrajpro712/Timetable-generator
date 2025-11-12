document.getElementById("generateBtn").addEventListener("click", async () => {
    const userGoals = document.getElementById("userGoals").value;
    const outputDiv = document.getElementById("scheduleOutput");
    outputDiv.innerHTML = "<p>⏳ Generating schedule...</p>";

    const response = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ goals: userGoals })
    });

    const data = await response.json();
    const schedule = data.schedule;

    outputDiv.innerHTML = "<h3>🕒 Your AI-Generated Schedule:</h3><ul>" +
        schedule.map(item => `<li>${item}</li>`).join('') +
        "</ul>";
});
