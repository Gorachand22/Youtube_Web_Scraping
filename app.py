from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import logging
from api_check import API
from yt_scraping import Scraping

app = Flask(__name__)
app.secret_key = 'mysecretkey123'
api = API()

# Configure logging
logging.basicConfig(filename='scrapper.log', level=logging.INFO)

# Enable CORS for all routes
CORS(app)

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/check_api', methods=["POST"])
@cross_origin()
def check_api():
    api_token = request.form.get('user_ka_api')
    try:
        response = api.check_api(api_token)
        if response == 1:
            return render_template('index2.html', message="Valid API Key, kindly proceed for scraping!")
        else:
            return render_template('index.html', message="Invalid API Key")
    except Exception as e:
        logging.error(f"API Key Check Error: {str(e)}")
        return render_template('index.html', message="An error occurred during API Key check. Please try again later.")

@app.route('/perform_scraping', methods=['POST'])
@cross_origin()
def perform_scraping():
    scarp_token = api.token
    ID = request.form.get('channel_id')
    try:
        video_data = Scraping.channel_playlist_id(scarp_token, ID)
        if video_data.empty:
            return render_template('output.html', video_data=None, message="No Results Found")
        else:
            return render_template('output.html', video_data=video_data)
    except Exception as e:
        logging.error(f"Scraping Error: {str(e)}")
        return render_template('output.html', video_data=None, message="An error occurred during scraping. Please try again later.")

if __name__ == '__main__':
    app.run(debug=True)
