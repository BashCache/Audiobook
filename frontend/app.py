import os
from flask import Flask,render_template,request
import tensorflow as tf
import cv2
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential,load_model
from deskewing import rotate_img, process_image_r,process_image
from median_filtering import median_subtract
from adaptive_threshold import adaptive_thresholding
import numpy as np
import matplotlib.pyplot as plt
from pdf2image import convert_from_path
from pdf2image.exceptions import ( PDFInfoNotInstalledError, PDFPageCountError, PDFSyntaxError )
import pytesseract
from pytesseract import Output
import imutils
from sort import natural_keys
from click_and_crop import main_func, click_and_crop
from PIL import Image
import re
from gtts import gTTS
from spellcheck import getEmail, getProperNoun, getURL, predict_word, basicRemoval, basicSpellCheck, finalIncorrectAndSuggested, replaceMASK, cleanupText, wordSplit

app = Flask(__name__)
print(tf.__version__)

graph = tf.compat.v1.get_default_graph()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
print('approot',APP_ROOT)

target = os.path.join(APP_ROOT, 'static', 'user-upload')
target_cleaned = os.path.join(APP_ROOT, 'static', 'cleaned-images')

if not os.path.isdir(target):
    os.mkdir(target)

if not os.path.isdir(target_cleaned):
    os.mkdir(target_cleaned)

@app.route('/')
def index():
    return render_template("upload.html")


@app.route("/upload", methods=['POST'])
def upload():

    print('form response: ', request.form["methods"])
    denoise_method = request.form["methods"]
    genre = request.form["genre"]
    
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = "/".join([target, filename])
        print('destination:',destination)
        file.save(destination)

        name_of_file = filename.split(".")
        type_of_file = name_of_file[1]
        print('only the filename', name_of_file)

        if not os.path.isdir(target+"/"+name_of_file[0]):
            os.mkdir(target+"/"+name_of_file[0])

        if not os.path.isdir(target_cleaned+"/"+name_of_file[0]):
            os.mkdir(target_cleaned+"/"+name_of_file[0])

        if genre == "newspaper":        # newspaper can only be images
            main_func(name_of_file[0], type_of_file, destination)

        elif type_of_file == 'jpg' or type_of_file == 'jpeg' or type_of_file == 'png':
            fname = name_of_file[0] + "." + type_of_file
            img = cv2.imread(destination)
            cv2.imwrite(target + "/" + name_of_file[0] + "/" + filename, img)
        #     if denoise_method == "median_filtering":
        #         dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+fname)
        #         rotated =  rotate_img(dirty_img)
        #         result, background = median_subtract(rotated)
        #         cv2.imwrite( target_cleaned + "/" + name_of_file[0]+ "/" + "med-" + fname, result)
            
        #     elif denoise_method == "adaptive_thresholding":
        #         dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+fname)
        #         rotated =  rotate_img(dirty_img)
        #         result = adaptive_thresholding(rotated)
        #         cv2.imwrite( target_cleaned + "/" + name_of_file[0]+ "/" + "adapt-" + fname, result)

        #     elif denoise_method == "autoencoders":
        #         # Rotate 
        #         array_image = []
        #         dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+fname)
        #         rotated =  rotate_img(dirty_img)
        #         result = rotated   # without median
        #         # result, background = median_subtract(rotated)  # with median
        #         # Process
        #         processed_image_list = process_image(result) # without median
        #         # processed_image_list = process_image_r(result) # with median
        #         processed_image_array = np.asarray(processed_image_list)
        #         new_X = np.expand_dims(processed_image_array, axis=0)
        #         print(processed_image_array.shape, new_X.shape)
        #         # Model.predict
        #         reconstructed_model = tf.keras.models.load_model('rms-final-model-200epochs')
        #         res = reconstructed_model.predict(new_X)
        #         plt.imsave( target_cleaned + "/" + name_of_file[0]+ "/" + "auto-" + fname, res[0][:,:,0], cmap='gray')
        #         # cv2.imwrite( './static/cleaned-images/' + filename, res)

        # #     file.save(target+"/"+name_of_file[0]+"/"+fname, type_of_file)

        # # print(images_1, type(images_1))
        
        elif type_of_file == 'pdf':
            images = convert_from_path(destination, poppler_path=r'C:/Users/admin/Downloads/poppler-0.68.0_x86/poppler-0.68.0/bin')
            print(type(images),images)
            for i, image in enumerate(images):
                fname = str(i) + "-" + name_of_file[0] + ".jpeg"
                image.save(target+"/"+name_of_file[0]+"/"+fname, "JPEG")

                # if denoise_method == "median_filtering":
                #     dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+fname)
                #     rotated =  rotate_img(dirty_img)
                #     result, background = median_subtract(rotated)
                #     cv2.imwrite( target_cleaned + "/" + name_of_file[0]+ "/" + "med-" + fname, result)
            
                # elif denoise_method == "adaptive_thresholding":
                #     dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+fname)
                #     rotated =  rotate_img(dirty_img)
                #     result = adaptive_thresholding(rotated)
                #     cv2.imwrite( target_cleaned + "/" + name_of_file[0]+ "/" + "adapt-" + fname, result)

                # elif denoise_method == "autoencoders":
                #     # Rotate 
                #     array_image = []
                #     dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+fname)
                #     rotated =  rotate_img(dirty_img)
                #     result = rotated   # without median
                #     # result, background = median_subtract(rotated)  # with median
                #     # Process
                #     processed_image_list = process_image(result) # without median
                #     # processed_image_list = process_image_r(result) # with median
                #     processed_image_array = np.asarray(processed_image_list)
                #     new_X = np.expand_dims(processed_image_array, axis=0)
                #     print(processed_image_array.shape, new_X.shape)
                #     # Model.predict
                #     reconstructed_model = tf.keras.models.load_model('rms-final-model-200epochs')
                #     res = reconstructed_model.predict(new_X)
                #     plt.imsave( target_cleaned + "/" + name_of_file[0]+ "/" + "auto-" + fname, res[0][:,:,0], cmap='gray')
                # # cv2.imwrite( './static/cleaned-images/' + filename, res)

    image_files = os.listdir(os.path.join(target, name_of_file[0]))
    image_files.sort(key=natural_keys)
    print(image_files)

    for i in range(len(image_files)):
        if denoise_method == "median_filtering":
            dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+image_files[i])
            rotated =  rotate_img(dirty_img)
            result, background = median_subtract(rotated)
            cv2.imwrite( target_cleaned + "/" + name_of_file[0]+ "/" + "med-" + image_files[i], result)
            
        elif denoise_method == "adaptive_thresholding":
            dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+image_files[i])
            rotated =  rotate_img(dirty_img)
            result = adaptive_thresholding(rotated)
            cv2.imwrite( target_cleaned + "/" + name_of_file[0]+ "/" + "adapt-" + image_files[i], result)

        elif denoise_method == "autoencoders":
            # Rotate 
            array_image = []
            dirty_img = cv2.imread(target+"/"+name_of_file[0]+"/"+image_files[i])
            rotated =  rotate_img(dirty_img)
            result = rotated   # without median
            # result, background = median_subtract(rotated)  # with median
            # Process
            processed_image_list = process_image(result) # without median
            # processed_image_list = process_image_r(result) # with median
            processed_image_array = np.asarray(processed_image_list)
            new_X = np.expand_dims(processed_image_array, axis=0)
            print(processed_image_array.shape, new_X.shape)
            # Model.predict
            reconstructed_model = tf.keras.models.load_model('rms-final-model-200epochs')
            res = reconstructed_model.predict(new_X)
            plt.imsave( target_cleaned + "/" + name_of_file[0]+ "/" + "auto-" + image_files[i], res[0][:,:,0], cmap='gray')
        # cv2.imwrite( './static/cleaned-images/' + filename, res)

    return render_template("denoise.html", filename = name_of_file[0], genre = genre)


@app.route('/ocr/<filename>+<genre>', methods=['POST','GET'])
def ocr(filename, genre):
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    print(pytesseract.get_tesseract_version())
    image_files = os.listdir(os.path.join(target_cleaned, filename))
    image_files.sort(key=natural_keys)
    print(image_files)

    i = 0
    file_ptr = open(os.path.join(target_cleaned, filename, filename) + ".txt", "a")

    for i in range(len(image_files)):
        print(image_files[i])
        img = cv2.imread(os.path.join(target_cleaned, filename, image_files[i]))
        newdata=pytesseract.image_to_osd(Image.open(os.path.join(target_cleaned, filename, image_files[i])), output_type=Output.DICT)
        print(newdata, newdata['rotate'], type(newdata), newdata['orientation'])
        # print(img)
        img = imutils.rotate_bound(img, newdata['rotate'])
        # angle=360-int(re.search('(?<=Rotate: )\d+', pytesseract.image_to_osd(Image.open(os.path.join(target_cleaned, filename, image_files[i])))).group(0))
        # print('anglle is: ', angle)
        # (h, w) = img.shape[:2]

        # if center is None:
        #     center = (w / 2, h / 2)
        # # Perform the rotation
        # M = cv2.getRotationMatrix2D(center, angle, scale)
        # rotated = cv2.warpAffine(img, M, (w, h))
        # cv2.imshow(img,"Properly rotated")
        # rot_data = pytesseract.image_to_osd(Image.open(os.path.join(target_cleaned, filename, image_files[i])));
        # print("[OSD] "+rot_data)
        # rot = re.search('(?<=Rotate: )\d+', rot_data).group(0)
        # angle = float(rot)
        # print('angle rotated: ', angle)

        # # Perform the rotation
        # M = cv2.getRotationMatrix2D(center, angle, scale)
        # rotated = cv2.warpAffine(img, M, (w, h))
        # cv2.imshow(img,"Properly rotated")

        # rotate the image to deskew it
        # rotated = imutils.rotate_bound(Image.open(os.path.join(target_cleaned, filename, image_files[i])), angle) #added


        # #  TODO: Rotated image can be saved here
        # print(pytesseract.image_to_osd(rotated));
        text = pytesseract.image_to_string(img, lang='eng')
        print(len(text))
        # print(text)
        file_ptr.write(text)
    
    file_ptr.close()
    return render_template("spellcheck.html", filename = filename, genre = genre)


@app.route('/spellchecker/<filename>+<genre>', methods=['POST'])    
def spellchecker(filename, genre):
    file_ptr = open(os.path.join(target_cleaned, filename, filename) + ".txt", "r")
    text = file_ptr.read()

    text_original = text
    text = basicRemoval(text)
    text = cleanupText(text)
    words = wordSplit(text)
    propernoun = getProperNoun(words)
    email = getEmail(words)
    url = getURL(words)
    incorrectwords, suggestedwords = basicSpellCheck(propernoun, email, url, words)
    final_incorrectwords, final_suggestedwords = finalIncorrectAndSuggested(incorrectwords, suggestedwords)
    text_replaced, text_original_replaced = replaceMASK(text, text_original, final_incorrectwords)
    text_original_final = predict_word(text_original_replaced, final_suggestedwords)

    file_ptr_masked = open(os.path.join(target_cleaned, filename, filename + "-masked") + ".txt", "a")
    file_ptr_masked.write(text_replaced)

    file_ptr_corrected = open(os.path.join(target_cleaned, filename, filename + "-corrected") + ".txt", "a")
    file_ptr_corrected.write(text_original_final)

    file_ptr.close()
    file_ptr_masked.close()
    file_ptr_corrected.close()
    # print(text)
    return render_template("text-to-speech.html", filename = filename, genre = genre)


@app.route('/audio/<filename>+<genre>', methods = ['POST'])
def audio(filename, genre):
    if genre == 'newspaper':
        file_ptr_corrected = open(os.path.join(target_cleaned, filename, filename ) + ".txt", "r")
    else:
        file_ptr_corrected = open(os.path.join(target_cleaned, filename, filename + "-corrected") + ".txt", "r")
    content = file_ptr_corrected.read()

    language = 'en'
    output = gTTS(text = content, lang = language)
    output.save(os.path.join(target_cleaned, filename, filename) + ".mp3")
    return render_template("play-audio.html", filename = os.path.join("../static/cleaned-images", filename, filename) + ".mp3", genre = genre)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
