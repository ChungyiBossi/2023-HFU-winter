import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2


def cvzone_face_detect(detector=FaceDetector(minDetectionCon=0.5, modelSelection=0)):
    # Initialize the webcam
    # '0' means the third camera connected to the computer, usually 0 refers to the built-in webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法開啟攝像頭。請確保攝像頭已正確連接。")
        exit()

    # Initialize the FaceDetector object
    # minDetectionCon: Minimum detection confidence threshold
    # modelSelection: 0 for short-range detection (2 meters), 1 for long-range detection (5 meters)
    # move to parameters

    # Run the loop to continually get frames from the webcam
    while True:
        # Read the current frame from the webcam
        # success: Boolean, whether the frame was successfully grabbed
        # img: the captured frame
        success, img = cap.read()

        # Detect faces in the image
        # img: Updated image
        # bboxs: List of bounding boxes around detected faces
        img, bboxs = detector.findFaces(img, draw=False)

        # Check if any face is detected
        if bboxs:
            # Loop through each bounding box
            for bbox in bboxs:
                # bbox contains 'id', 'bbox', 'score', 'center'

                # ---- Get Data  ---- #
                center = bbox["center"]
                x, y, w, h = bbox['bbox']
                score = int(bbox['score'][0] * 100)

                # ---- Draw Data  ---- #
                cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
                cvzone.putTextRect(img, f'{score}%', (x, y - 15), border=5)
                cvzone.cornerRect(img, (x, y, w, h))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Display the image in a window named 'Image'
        cv2.imshow("Image", img)
        # Wait for 1 millisecond, and keep the window open
        cv2.waitKey(1)


if __name__ in '__main__':
    cvzone_face_detect()
