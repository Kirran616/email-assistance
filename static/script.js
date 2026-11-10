const generateBtn = document.getElementById("generate");
const copyBtn = document.getElementById("copy");
const inputEl = document.getElementById("input");
const taskEl = document.getElementById("task");
const toneEl = document.getElementById("tone");
const outputCard = document.getElementById("output-card");
const outputEl = document.getElementById("output");
const errorEl = document.getElementById("error");

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.hidden = false;
}

generateBtn.addEventListener("click", async () => {
  errorEl.hidden = true;
  const text = inputEl.value.trim();
  if (!text) {
    showError("Please enter an email or message first.");
    return;
  }

  generateBtn.disabled = true;
  generateBtn.textContent = "Generating...";

  try {
    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, task: taskEl.value, tone: toneEl.value }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.error || "Something went wrong.");
    outputEl.textContent = data.result;
    outputCard.hidden = false;
    outputCard.scrollIntoView({ behavior: "smooth" });
  } catch (err) {
    showError(err.message);
  } finally {
    generateBtn.disabled = false;
    generateBtn.textContent = "Generate";
  }
});

copyBtn.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(outputEl.textContent);
    copyBtn.textContent = "Copied!";
  } catch {
    copyBtn.textContent = "Copy failed";
  }
  setTimeout(() => (copyBtn.textContent = "Copy"), 1500);
});
