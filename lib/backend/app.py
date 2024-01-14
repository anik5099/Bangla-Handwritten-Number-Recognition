import base64
import json
import os
import cv2
from flask import Flask, jsonify, request
from matplotlib import pyplot as plt
import numpy as np
from preprocessing import preprocessing
from flask_cors import CORS 
app = Flask(__name__)
CORS(app)
@app.route('/preprocessing', methods=['POST'])
def process():
 image_file = request.files['image']
 image_file.save('assets/hi.png')
 number ,img_list= preprocessing('assets/hi.png')
#  plt.imshow(img_list[0])
#  plt.show() 
 encoded_images = []
 for i, img in enumerate(img_list):
    try:
       
        img_array = np.asarray(img)
       
        img_array = (img_array * 255).astype(np.uint8)
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2BGR)

        
        encoded_image = base64.b64encode(cv2.imencode('.png', img_array)[1]).decode('utf-8')



        encoded_images.append(encoded_image)
    except Exception as e:
        print(f"Error processing image {i}: {e}")
     
 print(number)# Remove temporary file after processing
 number_list = number.tolist() if isinstance(number, np.ndarray) else number
 return jsonify({'number': number_list,'images':encoded_images}), 200

if __name__ == '__main__':
 app.run(debug=True)
