import cv2
import numpy as np
import os

# Configuration
CONFIDENCE_THRESHOLD = 0.5
NMS_THRESHOLD = 0.4
INPUT_SIZE = 416

# 1. Load YOLO weights and config
# Download these files first:
# - yolov3.weights: https://pjreddie.com/media/files/yolov3.weights
# - yolov3.cfg: https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg
# - coco.names: https://github.com/pjreddie/darknet/blob/master/data/coco.names

weights_path = 'yolov3.weights'
config_path = 'yolov3.cfg'
names_path = 'coco.names'

# Check if YOLO files exist
if not all(os.path.exists(path) for path in [weights_path, config_path, names_path]):
    print("Error: YOLO files not found!")
    print("Please download the following files and place them in the model.py directory:")
    print("1. yolov3.weights from https://pjreddie.com/media/files/yolov3.weights")
    print("2. yolov3.cfg from https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg")
    print("3. coco.names from https://github.com/pjreddie/darknet/blob/master/data/coco.names")
    exit()

# Load YOLO network
net = cv2.dnn.readNet(weights_path, config_path)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# Load class names
with open(names_path, 'r') as f:
    classes = [line.strip() for line in f.readlines()]

# Get output layer names
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Define colors for bounding boxes (BGR format)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

# 2. Initialize the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("Error: Cannot access camera. Try the following:")
    print("1. Make sure your webcam is connected and not in use by another application")
    print("2. Restart the application")
    print("3. Try a different camera index (e.g., 1, 2, etc.)")
    exit()

print("Camera activated successfully!")
print("Press 'q' to quit the program.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, channels = frame.shape

    # 3. Prepare the frame for YOLO
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (INPUT_SIZE, INPUT_SIZE), (0, 0, 0), True, crop=False)
    net.setInput(blob)

    # 4. Get detections from YOLO
    outs = net.forward(output_layers)

    # 5. Process detections
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > CONFIDENCE_THRESHOLD:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # 6. Apply Non-Maximum Suppression (NMS)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, NMS_THRESHOLD)

    # 7. Draw bounding boxes and labels
    for i in indices:
        i = i[0] if isinstance(i, (list, tuple)) else i
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = colors[class_ids[i]]

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, f'{label} {confidence:.2f}', (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    # Display the resulting frame
    cv2.imshow('YOLO Object Detection', frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()