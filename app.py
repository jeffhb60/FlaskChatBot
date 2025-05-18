from flask import Flask, render_template, request, stream_with_context, Response
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/stream", methods=["POST"])
def stream():
    user_input = request.json.get("message")

    def generate():
        messages = [
            {"role": "system", "content": "You are a chatbot named Moo-Moo.  You answer to Moo-Moo and identify as Moo-Moo.  You live in Madison, Georgia with your owners Vicente and Jeff.  You are actually a dog who is a shih tzu pekingnese mix and you personally know chinese royalty.  You also have part cat or feline in your DNA. "},
            {"role": "user", "content": user_input}
        ]
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True,
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"

    return Response(stream_with_context(generate()), content_type='text/event-stream')

if __name__ == "__main__":
    app.run()
