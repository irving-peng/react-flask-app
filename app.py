from flask import Flask
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('agg')
import io
from flask import (Flask, send_file,  redirect, render_template, request,
                   send_from_directory, url_for)
from flask import jsonify

app = Flask(__name__, static_folder='my-app/build', static_url_path='')
CORS(app)

@app.route('/api', methods=['GET'])
@cross_origin()
def index():
    return {
        "tutorial" : "Flask React Heroku"
    }

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')
    #return "hello world"

@app.route('/plot')
def plot():
    # Generate a simple plot
    plt.figure(figsize=(6, 4))
    plt.plot([1, 2, 3, 4], [1, 4, 2, 3], marker='o')
    plt.title('Sample Plot')

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()

    # Return the image file
    return send_file(img, mimetype='image/png')

@app.route('/submit-item', methods=['POST'])
def submit_item():
    data = request.get_json()
    item = data.get('item')
    # Process the item as needed
    print(f"Received item: {item}")
    # Send a response back to the client
    return jsonify({'status': 'success', 'item': item})

if __name__ == '__main__':
    app.run()