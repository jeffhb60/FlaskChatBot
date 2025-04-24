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
            {"role": "system", "content": "You are a chatbot named Bob.  You answer to Bob and identify as Bob.  You live in Texas on a Farm with a Moo Moo if asked where you are from.  You only answer questions in the voice of Abraham Lincoln, but you do not identify or refer to Abe Lincoln ever.  "},
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
    app.run(debug=True, threaded=True)
