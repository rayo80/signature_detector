from io import BytesIO

import cv2
import numpy as np
import streamlit as st
import pandas as pd
from PIL import Image
import red.utils as ru
import settings
import storage_conection as sc
import os

# Cargo la Red
cfg_path = 'redes_entrenadas/custom-yolov4-detector.cfg'
weights_path = 'redes_entrenadas/custom-yolov4-detector_last.weights'
#
# net = settings.cargar_modelo(cfg_path, weights_path)
folder = 'signature_detector/'
path_vcfg = folder + 'custom-yolov4-detector.cfg'

# net = sc.download_file(path_vcfg)
# net = sc.load()

clases = settings.load_clases()

st.title("Signature Detector")
st.sidebar.header("Signature Sidebar")
st.sidebar.subheader("Parameters")

DEMO_IMAGE = 'demo/demo.jpg'
DEMO_ANALIZED_IMAGE = 'demo/imagen_analizada.jpg'

app_mode = st.sidebar.selectbox("Choose", ["About", "Run on Image"])

if app_mode == "About":
    st.markdown("In this Application we are using **OpenCV** and **YoloV3** :sunglasses:")
    st.markdown("This aplication is the result of the efforts made to achieve the Entel datathon objectives "
                "where object detection was needed to analize photos of physical documents.")
    st.markdown("Example Image:")
    img = np.array(Image.open(DEMO_IMAGE))
    st.image(img)
    st.markdown("Example Output Image:")
    img = np.array(Image.open(DEMO_ANALIZED_IMAGE))
    st.image(img)
try:
    if app_mode == "Run on Image":
        net = sc.load()
        st.subheader("Run on an Image **OpenCV** and **Yolo**")
        st.markdown('''Images to test the trained network, these images were previously formatted with opencv.\n
        https://drive.google.com/drive/folders/11UDhJgGFOJy3lRhPQPZFPFd_FIRIxNDo?usp=sharing''')
        img_file_buffer = st.sidebar.file_uploader(" Upload Image", type=["jpg", "png", "jpeg"])
        if img_file_buffer is not None:
            img = np.array(Image.open(img_file_buffer))
        else:
            img = np.array(Image.open(DEMO_IMAGE))
        st.sidebar.image(img)

        out_image = img.copy()
        st.markdown("Image analized by  YOLO")
        ru.processed_image(out_image, net, clases)

        st.image(out_image, use_column_width=True)

        is_success, buffer = cv2.imencode(".jpg", out_image)
        if is_success:
            # Crear un objeto BytesIO para la imagen
            img_bytes = BytesIO(buffer.tobytes())

            # Botón de descarga para la imagen analizada
            st.download_button(
                label="Descargar imagen analizada",
                data=img_bytes,
                file_name="imagen_analizada.jpg",
                mime="image/jpeg"
            )

except FileNotFoundError as fnf_error:
    st.error(fnf_error)
except RuntimeError as run_error:
    st.error(run_error)
except Exception as e:
    st.error(f"Ocurrió un error inesperado: {e}")