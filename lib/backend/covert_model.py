import tensorflow as tf
model = tf.keras.models.load_model('cnn.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('assets/model.tflite', 'wb') as f:
  f.write(tflite_model)