from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import json
import os

app = Flask(__name__)

# Greeting words
greetings = ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]

# Gemini API configuration
genai.configure(api_key="YOUR_API_KEY_HERE")

model = genai.GenerativeModel("gemini-2.5-flash")

CHAT_FILE = "chat_history.json"


# Create JSON file if it does not exist
if not os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "w") as f:
        json.dump({"chats": []}, f)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Get chat history (for left panel)
@app.route("/history")
def history():

    with open(CHAT_FILE, "r") as file:
        data = json.load(file)

    return jsonify(data)


# Chatbot API
@app.route("/chat", methods=["POST"])
def chat():

    data = request.json
    user_message = data.get("message", "").lower()

    # Greeting detection
    if any(word in user_message for word in greetings):
        return jsonify({
            "reply": "Hey 👋 How can I help you today with farming?"
        })

    # Thank response
    if "thank" in user_message:
        return jsonify({
            "reply": "You're welcome! 🌱 Let me know if you need farming advice."
        })

    # Bye response
    if "bye" in user_message:
        return jsonify({
            "reply": "Goodbye! Have a great farming day 🚜🌾"
        })


    prompt = f"""
You are a Farmer Agriculture Advisor AI.

Your job:
- Answer ONLY about farming and agriculture.
- Give crop suggestions based on seasons.
- Explain in simple language for farmers.

Important Rule:
If the user asks anything unrelated to agriculture
(example: programming, health, education, python, movies etc)

You must reply ONLY with:
"I am trained only to give farmer agriculture suggestions based on seasons."

User Question: {user_message}
"""

    try:

        response = model.generate_content(prompt)
        bot_reply = response.text


        # Load chat history
        with open(CHAT_FILE, "r") as file:
            chat_data = json.load(file)


        # Add new chat
        chat_data["chats"].append({
            "user": user_message,
            "bot": bot_reply
        })


        # Save chat history
        with open(CHAT_FILE, "w") as file:
            json.dump(chat_data, file, indent=4)


        return jsonify({
            "reply": bot_reply
        })


    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)