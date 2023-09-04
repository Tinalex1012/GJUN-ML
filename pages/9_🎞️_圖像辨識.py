import streamlit as st 
from skimage import data, color, io
from skimage.transform import rescale, resize, downscale_local_mean

import numpy as np  
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json
import cv2

IMAGE_SIZE = (150,150)
out_labels = ['建築物','森林','冰川','山景','海景','街景']
model = tf.keras.models.load_model('./MODEL/OUT_MODEL')
st.title("Intel圖像辨識")

uploaded_file = st.file_uploader("上傳圖片(.jpg)", type="jpg")
if uploaded_file is not None:
    X0 = io.imread(uploaded_file)
    X1 = cv2.cvtColor(X0, cv2.COLOR_BGR2RGB)
    X1 = cv2.resize(X1, IMAGE_SIZE) 
    X1 = np.array(X1, dtype = 'float32') / 255.0

    X2 = X1.reshape(1,X1.shape[0],X1.shape[1],X1.shape[2])
    # 預測
    st.write("辨識")
    predictions = np.argmax(model.predict(X2), axis=-1)
    st.markdown(f"# {out_labels[predictions[0]]}")
    st.image(uploaded_file)