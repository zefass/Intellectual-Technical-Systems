import cv2
import numpy as np

net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg.txt")
CLASSES = {0: 'person', 39: 'bottle'}
COLORS = {0: (255, 0, 255), 39: (255, 255, 0)}

CONFIDENCE = 0.5
THRESHOLD = 0.3
FPS_LIMIT = 30

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        (H, W) = frame.shape[:2]

        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        ln = net.getLayerNames()
        ol = [ln[i - 1] for i in net.getUnconnectedOutLayers()]
        layerOutputs = net.forward(ol)

        boxes = []
        confidences = []
        classIDs = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                if CLASSES.get(classID) is None:
                    continue

                if confidence > CONFIDENCE:
                    box = detection[0:4] * np.array([W, H, W, H])
                    (centerX, centerY, width, height) = box.astype("int")
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE,
                                THRESHOLD)
        people = list()
        bottles = list()
        if len(idxs) > 0:
            for i in idxs.flatten():
                (x, y) = (boxes[i][0], boxes[i][1])
                (w, h) = (boxes[i][2], boxes[i][3])

                if CLASSES.get(classIDs[i]) == 'person':
                    people.append((x, y, w, h))
                if CLASSES.get(classIDs[i]) == 'bottle':
                    bottles.append((x, y, w, h))

                color = [int(c) for c in COLORS.get(classIDs[i])]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                text = "{}: {:.4f}".format(CLASSES.get(classIDs[i]), confidences[i])
                cv2.putText(frame, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.5, color, 2)

        for bottle in bottles:
            bx, by, bw, bh = bottle
            for person in people:
                px, py, pw, ph = person
                if (bx > px) and (by > py) and (bx + bw < px + pw) and (by + bh < py + ph):
                    cv2.putText(frame, 'Look at him drinking', (px+250, py-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0),
                                2)

        cv2.imshow("Frame", frame)

        if cv2.waitKey(1000//FPS_LIMIT) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()