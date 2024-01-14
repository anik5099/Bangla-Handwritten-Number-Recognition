from keras.models import load_model
from matplotlib import pyplot as plt
import numpy as np
import cv2
from PIL import Image

def preprocessing(path):
    model = load_model('cnn.h5')
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    inverted_image = cv2.bitwise_not(image)
    # inverted_image  = inverted_image[:, :, 0]
    inverted_image = (inverted_image >= 0.5).astype(int)
    (row, col) = inverted_image.shape
    flag = False
    start = []
    end = []
    for i in range(col):
        sum = 0
        for j in range(row):
            sum += inverted_image[j][i]
        if sum != 0 : 
            if flag == False :
                start.append(i-2)
                flag = True
        else:
            if flag == True :
                end.append(i+2)
                flag = False

    number = 0
    l = []
    for i in range(len(start)):
        digit = inverted_image[:, start[i]:end[i]]
        digit = digit.astype(np.uint8)  
        pil_image = Image.fromarray(digit)
        
        new_shape = (32, 32)
        resized_digit = cv2.resize(digit, new_shape, interpolation=cv2.INTER_CUBIC)

        reshaped_digit = resized_digit.reshape(-1, 32, 32, 1)
        # plt.imshow(reshaped_digit[0, :, :, 0], cmap='gray')
        # plt.show()
        l.append(pil_image)
        pred = model.predict(reshaped_digit)
        predicted_labels = np.argmax(pred, axis=1)
        number = number * 10 + predicted_labels

    return number,l
