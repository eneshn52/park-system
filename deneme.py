import cv2
import numpy as np
import cvzone

# Video yolu → BURAYI KENDİ YOLUNLA GÜNCELLE
video_path = r"C:\Users\eeshn\Desktop\carparkk.mp4"
cap = cv2.VideoCapture(video_path)

# 6 park yeri için koordinatlar (görüntüye göre ayarlandı)
posList = [ ((155, 300), (280, 390)),
    ((305, 300), (430, 390)),
    ((455, 300), (580, 390)),
    ((605, 300), (730, 390)),
    ((755, 300), (880, 390)),
    ((905, 300), (1030, 390))]  # engelli yeri

def checkParkingSpace(imgPro, img):
    spaceCounter = 0

    for i, (start, end) in enumerate(posList):
        x1, y1 = start
        x2, y2 = end

        x, y = min(x1, x2), min(y1, y2)
        w, h = abs(x2 - x1), abs(y2 - y1)

        imgCrop = imgPro[y:y + h, x:x + w]
        count = cv2.countNonZero(imgCrop)

        if count < 900:
            color = (0, 255, 0)  # boş - yeşil
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)  # dolu - kırmızı
            thickness = 2

        cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)

    # ekran üstü yazı
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}',
                       (100, 50), scale=3, thickness=5, offset=20, colorR=(0, 200, 0))

while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        print("Video okunamadı.")
        break

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate, img)

    cv2.imshow("Parking Detection", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
