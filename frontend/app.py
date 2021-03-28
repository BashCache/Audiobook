import os
from flask import Flask,render_template,request
import tensorflow as tf
import cv2
# from tensorflow import keras
from tensorflow.keras.models import Model, Sequential,load_model
from deskewing import rotate_img
from median_filtering import median_subtract
from adaptive_threshold import adaptive_thresholding

app = Flask(__name__)
print(tf.__version__)

graph = tf.compat.v1.get_default_graph()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print('approot',APP_ROOT)

@app.route('/')
def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])
def upload():
    # print('request in upload', request)
    target = os.path.join(APP_ROOT, 'static', 'user-upload')
    # print('target',target)
    # reconstructed_model = tf.keras.models.load_model('temp-check')
    if not os.path.isdir(target):
        os.mkdir(target)
    
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        print('destination:',destination)
        file.save(destination)
    
    print('form response: ', request.form["methods"])
    denoise_method = request.form["methods"]

    if denoise_method == "median_filtering":
        dirty_img = cv2.imread(destination)
        rotated =  rotate_img(dirty_img)
        result, background = median_subtract(rotated)
        cv2.imwrite( './static/cleaned-images/' + filename, result)
        return render_template("finish.html", denoised_image = './static/cleaned-images/' + filename)

    elif denoise_method == "adaptive_thresholding":
        dirty_img = cv2.imread(destination)
        rotated =  rotate_img(dirty_img)
        result = adaptive_thresholding(rotated)
        cv2.imwrite( './static/cleaned-images/' + filename, result)
        return render_template("finish.html", denoised_image = './static/cleaned-images/' + filename)


    elif denoise_method == "autoencoders":
        # Rotate 
        # Process
        # Model.predict
        print(1)
        
    return render_template("finish.html", denoised_image = './static/cleaned-images/' + filename)

if __name__ == "__main__":
    app.run(port=3000, debug=True)



# ALWAYS STORE IMAGES IN STATIC FOLDER ONLY