import os
import cv2

cfg_path = 'redes_entrenadas1/custom-yolov4-detector.cfg'
weights_path = 'redes_entrenadas1/custom-yolov4-detector_last.weights'


def cargar_modelo(cfg_path, weights_path):
    if not os.path.exists(cfg_path):
        raise FileNotFoundError(f"El archivo de configuración no se encontró: {cfg_path}")
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"El archivo de pesos no se encontró: {weights_path}")

    try:
        net = cv2.dnn.readNetFromDarknet(cfg_path, weights_path)
        net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        return net
    except cv2.error as e:
        raise RuntimeError(f"Error al cargar el modelo: {e}")


def load_clases():
    with open("redes_entrenadas/coco.names", 'r') as f:
        classes = f.read().splitlines()
    return classes

