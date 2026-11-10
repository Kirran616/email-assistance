# AI Email Assistant

Generate professional replies, rewrite informal messages, summarize long emails and draft follow-ups.
Stack: Python 3.11 + Flask, HTML/CSS/JavaScript, OpenRouter API (`openai/gpt-4o-mini`).

## Setup in VS Code

1. Unzip the folder and open it in VS Code (File > Open Folder).
2. Open the terminal (Ctrl + `) and create a virtual environment:

   Windows:
   ```
   py -3.11 -m venv venv
   venv\Scripts\activate
   ```
   macOS/Linux:
   ```
   python3.11 -m venv venv
   source venv/bin/activate
   ```
   (If PowerShell blocks activation, run: `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`)

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and paste your OpenRouter API key
   (create one at https://openrouter.ai/keys).
5. Run the app:
   ```
   python app.py
   ```
6. Open http://127.0.0.1:5000 in your browser.

## Project structure

```
ai-email-assistant/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── templates/index.html
└── static/
    ├── style.css
    └── script.js
```

## Notes
- Never commit your `.env` file or share your API key.
- Change the model any time by editing `OPENROUTER_MODEL` in `.env`.
