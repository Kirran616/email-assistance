import os
import requests
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

TASK_PROMPTS = {
    "reply": "Write a professional, polite and clear reply to the email or message below. Return only the email text, including a subject line if appropriate.",
    "rewrite": "Rewrite the informal message below as a polished, professional email. Keep the original meaning. Return only the email text.",
    "summarize": "Summarize the email below in a short paragraph, then list any action items as bullet points.",
    "followup": "Write a polite, professional follow-up email based on the email or message below. Return only the email text.",
}

TONES = {"professional", "friendly", "formal", "concise"}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/generate", methods=["POST"])
def generate():
    if not OPENROUTER_API_KEY:
        return jsonify({"error": "Missing OPENROUTER_API_KEY. Add it to your .env file."}), 500

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    task = data.get("task", "reply")
    tone = data.get("tone", "professional")

    if not text:
        return jsonify({"error": "Please enter an email or message."}), 400
    if len(text) > 8000:
        return jsonify({"error": "Text is too long (max 8000 characters)."}), 400
    if task not in TASK_PROMPTS:
        return jsonify({"error": "Invalid task."}), 400
    if tone not in TONES:
        tone = "professional"

    system_prompt = (
        "You are an expert email writing assistant. "
        f"{TASK_PROMPTS[task]} Use a {tone} tone."
    )

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0.7,
        "max_tokens": 800,
    }
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        resp = requests.post(API_URL, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        output = result["choices"][0]["message"]["content"].strip()
        return jsonify({"result": output})
    except requests.exceptions.HTTPError:
        try:
            msg = resp.json().get("error", {}).get("message", "API request failed.")
        except Exception:
            msg = "API request failed."
        return jsonify({"error": msg}), 502
    except requests.exceptions.RequestException:
        return jsonify({"error": "Could not reach OpenRouter. Check your internet connection."}), 502
    except (KeyError, IndexError, ValueError):
        return jsonify({"error": "Unexpected response from the AI service."}), 502


if __name__ == "__main__":
    app.run(debug=True)
