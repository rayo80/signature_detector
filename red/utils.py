import cv2
import numpy as np
import matplotlib.pyplot as plt

# section_detect = cv2.dnn.readNet(
#     'redes_entrenadas/custom-yolov4-detector.cfg',
#     'redes_entrenadas/custom-yolov4-detector_last.weights')


# classes = ['fecha', 'firma1', 'firma2']
# colors = np.random.uniform(0, 255, size=(len(classes), 3))


class Box:
    def __init__(self, box: list, confidence: float, class_id: int):
        self.figura = box
        self.confidence = confidence
        self.class_id = class_id


def draw_boxes(img, boxes: list[Box], clases: list):
    colors = np.random.uniform(0, 125, size=(len(clases), 3))
    for i, b in enumerate(boxes):
        x, y, w, h = b.figura
        label = str(clases[b.class_id]) + ' :' + str(int(b.confidence*100)) + '%'
        color = colors[i]
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
        cv2.putText(img, label, (x, y - 15), cv2.FONT_HERSHEY_PLAIN, 2, color, 2)
    return img


def get_boxes(img, section_detect):
    height, width = img.shape[:2]
    blob = cv2.dnn.blobFromImage(img, scalefactor=1 / 255,
                                 size=(416, 416), mean=(0, 0, 0), swapRB=True, crop=False)
    section_detect.setInput(blob)
    output_layer_names = section_detect.getUnconnectedOutLayersNames()  # obtiene la lista de las capas finales
    layerout = section_detect.forward(output_layer_names)  # obtiene el valor de salida de las capas indicadas.

    boxes = []
    confidences = []
    class_ids = []
    cajas = []

    for output in layerout:  # entra en layerout , en output hay un monton de arrays q representan cajas
        for detection in output:
            score = detection[5:]  # detection array de len 8 (x,y,w,h,  luego 3 scores por ser 3 obj)
            class_id = np.argmax(score)  # Identifica el id de clase segun la máxima confianza dentro de score
            confidence = score[class_id]
            if confidence > 0.8:
                # La caja detectada
                center_x = int(detection[0] * width)  # convertimos el centro x
                center_y = int(detection[1] * height)  # convertimos el centro y
                w = int(detection[2] * width)  # el ancho se multiplica por el valor de la imagen original
                h = int(detection[3] * height)  # el alto se multiplica por el valor de la imagen original
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                box = [x, y, w, h]
                boxes.append(box)  # cajas en la imagen original
                confidences.append(float(confidence))
                class_ids.append(class_id)
                caja = Box(box, float(confidence), class_id)
                cajas.append(caja)

    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.5, nms_threshold=0.4)
    # indeces me devuelve los indices de las cajas que considerare
    filtered_cajas = [cajas[i] for i in indices]

    return filtered_cajas


def processed_image(image, net, clases):
    boxes = get_boxes(image, net)
    img_output = draw_boxes(image, boxes, clases)
    return img_output
