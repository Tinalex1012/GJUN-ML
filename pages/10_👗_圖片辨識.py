import streamlit as st 
from skimage import data, color, io
from skimage.transform import rescale, resize, downscale_local_mean

import numpy as np  
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json

out_labels = ['短袖汗衫','褲子','套衫','裙子','外套','涼鞋','襯衫','運動鞋','包包','長靴']
model = tf.keras.models.load_model('./MODEL/fashion_model.h5')

st.title("上傳女性飾品圖片辨識")

uploaded_file = st.file_uploader("上傳圖片(.jpg)", type="jpg")
if uploaded_file is not None:
    image1 = io.imread(uploaded_file, as_gray=True)
    image_resized = resize(image1, (28, 28), anti_aliasing=True)    
    X1 = image_resized.reshape(1,28, 28) #/ 255
    X1 = np.abs(1-X1)
    st.write("辨識")
    predictions = np.argmax(model.predict(X1), axis=-1)
    st.markdown(f"#  {out_labels[predictions[0]]}")
    st.image(image1)
