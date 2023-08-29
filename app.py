# pip install streamlit
# pip install streamlit-drawable-canvas
import streamlit as st 
from streamlit_drawable_canvas import st_canvas
from skimage import data, color, io
from skimage.transform import rescale, resize, downscale_local_mean
from skimage.color import rgb2gray, rgba2rgb

import numpy as np  
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import model_from_json

# 模型載入
model = tf.keras.models.load_model('Emnist_model.h5')

col1, col2 = st.columns(2)

with col1:
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 1)",
        stroke_width=10,
        stroke_color="rgba(0, 0, 0, 1)",
        update_streamlit=True,
        width=280,
        height=280,
        drawing_mode="freedraw",
        key="canvas1",
    )

with col2:
    if st.button('辨識'):
        # print(canvas_result.image_data.shape)
        image1 = rgb2gray(rgba2rgb(canvas_result.image_data))
        image_resized = resize(image1, (28, 28), anti_aliasing=True)  
        # print(image_resized)
        X1 = image_resized.reshape(1,28,28) # / 255
        X1 = np.abs(1-X1)
        
        st.write("predict...")
        predictions = np.argmax(model.predict(X1), axis=-1)
        st.write('# ' + chr(ord('A')+predictions[0]))
        st.image(image_resized)
