from flask import Flask, request, render_template
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
# from PIL import Image

import os

app = Flask(__name__)


def load_my_model(model_path):
    try:
        model = load_model(model_path)
        print("Model loaded successfully!")
        return model
    except OSError as e:
        print(f"Error loading model: {e}")
        return None

# def convert_image_to_jpg(image_path, output_path):
#     with Image.open(image_path) as img:
#         rgb_img = img.convert('RGB')
#         rgb_img.save(output_path, 'JPEG')


def prepare_image(img_path):
    img = image.load_img(img_path, target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0
    return img_array


model = load_my_model('model.h5')


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return "<p id='prediction' class='flex items-center justify-center w-96 p-4 mt-4 bg-white shadow-md rounded-lg text-red-800 font-bold'>No image part in the form</p>"

    image_file = request.files['image']
    image_file.save('image.jpg')

    try:
        img = prepare_image('image.jpg')
        predictions = model.predict(img)
        predicted_class = np.argmax(predictions, axis=1)[0]
        class_names = ['airplane', 'automobile', 'bird', 'cat',
                       'deer', 'dog', 'frog', 'horse', 'ship', 'truck']
        class_name = class_names[predicted_class]
        os.remove('image.jpg')
        return "<p id='prediction' class='flex items-center justify-center w-96 p-4 mt-4 bg-white shadow-md rounded-lg text-gray-800 font-bold'>" + class_name.capitalize() + "</p>"
    except Exception as e:
        return "<p id='prediction' class='flex items-center justify-center w-96 p-4 mt-4 bg-white shadow-md rounded-lg text-red-800 font-bold'>Error predicting image</p>"


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8080)
