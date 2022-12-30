from flask import Flask, render_template, request
from model import chatbot

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    result = chatbot(userText)
    return result
    
if __name__ == "__main__":
    app.run()