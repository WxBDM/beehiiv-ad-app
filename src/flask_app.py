from flask import Flask, render_template, send_from_directory, render_template_string
import os
import random
app = Flask(__name__, template_folder='/home/bmolyneaux/pysnax_ads/templates')

THIS_DIR = os.path.dirname(__file__)

# Directory where banner images are stored
IMAGE_DIR = os.path.join(THIS_DIR, 'ad_images')
# if needed, just use /ad_images/10-python-list-methods-thumbnail.png

@app.route('/get-ad')
def serve_ad():
    # List all files in the image directory
    available_ads = os.listdir(IMAGE_DIR)
    # Randomly select an ad from the directory
    selected_ad = random.choice(available_ads)
    # Serve the randomly selected ad image with no caching
    response = send_from_directory(IMAGE_DIR, selected_ad)
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/ad-content')
def ad_content():
    # Dynamically generate the URL each time to avoid caching issues
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Advertisement</title>
    </head>
    <body style="margin: 0; padding: 0; overflow: hidden;">
        <!-- Dynamically loaded image to take full size of iframe, src set to get-ad route -->
        <img src="https://bmolyneaux.pythonanywhere.com/get-ad" style="width: 100%; height: auto;" alt="Advertisement Banner">
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run()
