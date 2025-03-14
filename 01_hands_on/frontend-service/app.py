from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    response = requests.get('http://backend-service:5000')
    return f"The backend said: {response.text}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)