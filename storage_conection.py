from google.cloud import storage
import os
import tempfile
import cv2
import streamlit as st

bucket_name = "svm-docs"
folder = 'signature_detector/'


@st.cache_resource
def load(bucket_name=bucket_name):
    """Descarga un archivo desde Google Cloud Storage a un destino local."""
    # Inicializa el cliente de almacenamiento
    cfg_blob_name = folder + 'custom-yolov4-detector.cfg'
    weights_blob_name = folder + 'custom-yolov4-detector_last.weights'
    cfg_bytes = download_blob(cfg_blob_name, bucket=bucket_name)
    weights_bytes = download_blob(weights_blob_name, bucket=bucket_name)
    # Crear archivos temporales para cfg y weights
    with tempfile.NamedTemporaryFile(delete=False, suffix='.cfg') as cfg_file:
        cfg_file.write(cfg_bytes)
        cfg_path = cfg_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix='.weights') as weights_file:
        weights_file.write(weights_bytes)
        weights_path = weights_file.name

    net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
    os.remove(cfg_path)
    os.remove(weights_path)
    return net


def get_storage_client():
    if os.environ['SETTINGS'] == 'local':
        print("aqui entre")
        GOOGLE_APPLICATION_CREDENTIALS = 'cloud_conections.json'
        return storage.Client.from_service_account_json(GOOGLE_APPLICATION_CREDENTIALS)
    else:
        # return google.auth.default()[0]
        return storage.Client(bucket_name)


def download_blob(filename, bucket=None):
    storage_client = get_storage_client()
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(filename)
    return blob.download_as_bytes(raw_download=True)


def asegurar_archivo_local(bucket_name, source_blob_name, local_path):
    """Asegura que el archivo esté disponible localmente."""
    if not os.path.exists(local_path):
        download_file(bucket_name, source_blob_name, local_path)
    else:
        print(f"El archivo {local_path} ya existe localmente.")

