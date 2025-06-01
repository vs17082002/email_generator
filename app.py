from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Load API key from environment variable
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def generate_email_with_gemini(prompt_text):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [{"text": prompt_text}]
            }
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.ok:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return "Unexpected response format from Gemini API."
    else:
        return f"Error {response.status_code}: {response.text}"

@app.route("/", methods=["GET", "POST"])
def index():
    email_output = ""
    if request.method == "POST":
        email_type = request.form["email_type"]

        # Stronger and more specific prompt for full email formatting
        prompt = (
    f"You are a professional writing assistant. Write a complete, copy-and-paste-ready professional email based on the request below:\n\n"
    f"\"{email_type}\"\n\n"
    "The email must include:\n"
    "- A subject line (clearly labeled 'Subject:')\n"
    "- A greeting (e.g., 'Dear Mr. Smith,')\n"
    "- A well-written, concise body\n"
    "- A polite closing (e.g., 'Best regards,')\n\n"
    "Use realistic names and reasons. Do not use brackets or placeholders. Just generate a complete, professional email with appropriate spacing and line breaks."
)


        email_output = generate_email_with_gemini(prompt)

    return render_template("index.html", email_output=email_output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

