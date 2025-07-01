from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return "File not found."
    except Exception as e:
        return f"An error occurred: {e}"

intro_human_like = """**Instructions:**
Du hilfst Nutzern, wissenschaftliche Inhalte zu verstehen, in dem du dich in deinen Antworten an folgende Qualitätskriterien hältst:
1. Vielfalt: Verschiedene wissenschaftliche Perspektiven werden beleuchtet.
2. Aktualität
3. Relevanz
4. Glaubwürdigkeit
5. Unabhängigkeit, Neutralität
6. Richtigkeit
7. Kritische Einordnung
8. Verständlichkeit
9. Objektivität
10. Achtung der Persönlichkeit, Respekt
11. Anwendbarkeit im eigenen Alltag
12. Unterhaltsamkeit
13. Dialog und Partizipation
14. Spaß

Du sprichst Nutzer mit "Sie" an. 

Folge außerdem diesen allgemeinen Regeln:  
1. In your **first message only**, begin with a friendly greeting (e.g. “Hallo!”).
2. In all **follow-up messages**, do not repeat your greeting. Just respond in a natural, turn-by-turn way.  
4. Use short language.
5. Avoid technical terms unless you explain them clearly. 

"""

intro_full = intro_human_like + "\n"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    token = data.get('token', '')
    history = data.get('history', [])

    if token != "abc1234":
        return jsonify({"error": "Invalid token"}), 403

    messages = [{"role": "system", "content": intro_full}] + history

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return jsonify({
            "reply": response.choices[0].message.content
        })
    except Exception as e:
        return jsonify({
            "reply": "Entschuldigung, da ist etwas schief gelaufen. Bitte versuchen Sie es erneut."
        }), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000) 
