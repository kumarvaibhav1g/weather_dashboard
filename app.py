import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("WEATHERAPI_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    if request.method == 'POST':
        city = request.form['city']
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"
        response = requests.get(url)
        data = response.json()

        if "current" in data:
            weather_data = {
                'city': data['location']['name'],
                'country': data['location']['country'],
                'temperature': data['current']['temp_c'],
                'condition': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon']
            }
        else:
            error = data.get("error", {}).get("message", "City not found.")

    return render_template('index.html', weather=weather_data, error=error)

if __name__ == "__main__":
    app.run(debug=True)
