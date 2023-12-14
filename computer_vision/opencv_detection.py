import cv2


def opencv_detect_with_image(image_path, cascade_classifier):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)   # 將圖片轉成灰階
    results = cascade_classifier.detectMultiScale(gray)    # 偵測

    for (x, y, w, h) in results:  # x,y 框框左上的點, w是寬度, h是高度
        cv2.rectangle(
            img, (x, y), (x+w, y+h), (0, 255, 0), 2
        )    # 利用 for 迴圈，繪製方框
    cv2.imshow('oxxostudio', img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()


def opencv_detect_with_webcam(model_path):
    face_cascade = cv2.CascadeClassifier(model_path)   # 載入模型
    # 讀鏡頭
    # 打開攝像頭
    cap = cv2.VideoCapture(0)  # 0代表默認攝像頭，如果有多個攝像頭，可以嘗試1、2、3等
    # 設定視訊窗口的大小
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    # 檢查攝像頭是否成功打開
    if not cap.isOpened():
        print("無法開啟攝像頭。請確保攝像頭已正確連接。")
        exit()
    while True:
        # 讀取一幀的視訊
        ret, frame = cap.read()
        # 檢查視訊是否成功讀取
        if not ret:
            print("無法獲取視訊幀。")
            break
        # 用當前的 frame 送去偵測
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)   # 將圖片轉成灰階
        faces = face_cascade.detectMultiScale(gray)    # 偵測人臉

        for (x, y, w, h) in faces:  # x,y 框框左上的點, w是寬度, h是高度
            cv2.rectangle(
                frame, (x, y), (x+w, y+h), (0, 255, 0), 2
            )    # 利用 for 迴圈，抓取每個人臉屬性，繪製方框
        cv2.imshow('oxxostudio', frame)
        # 按 'q' 鍵退出迴圈
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # 釋放攝像頭資源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    model_path = 'haarcascade_frontalface_default.xml'
    opencv_detect_with_webcam(model_path)

    image_path = 'test_images/test_tm_2.jpeg'
    face_cascade = cv2.CascadeClassifier(model_path)   # 載入模型
    opencv_detect_with_image(image_path, face_cascade)
