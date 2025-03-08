import cv2
import matplotlib.pyplot as plt
import numpy as np
from ultralytics import YOLO

# Görüntüyü yükleme
image_path = r"C:\Users\eeshn\Desktop\carParkImg.png"
image = cv2.imread(image_path)

# Görüntüyü BGR'den RGB'ye çevirme
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Park alanlarını depolamak için liste
parking_spots = []

def select_parking_spot(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Seçilen alanın koordinatlarını kaydetme
        w, h = 80, 40  # Sabit genişlik ve yükseklik değerleri
        parking_spots.append((x, y, w, h))
        cv2.rectangle(image_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow('Park Alanlarını Belirle', cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))

# Pencere oluşturma ve mouse callback fonksiyonunu bağlama
cv2.imshow('Park Alanlarını Belirle', cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
cv2.setMouseCallback('Park Alanlarını Belirle', select_parking_spot)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Seçilen park alanlarını gösterme
plt.figure(figsize=(10, 10))
plt.imshow(image_rgb)
plt.axis('off')
plt.show()

print(f"{len(parking_spots)} park alanı manuel olarak belirlendi.")

# YOLO modelini yükleme
model = YOLO('yolov8n.pt')  # YOLOv8 nano pre-trained modeli

# Video yolu
video_path = r"C:\Users\eeshn\Desktop\carPark.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Video açılamadı!")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO ile araç tespiti
    results = model(frame)

    # Araç tespiti için bounding box'ları al
    for result in results.pred[0]:
        x1, y1, x2, y2, conf, cls = result
        if int(cls) == 2 or int(cls) == 7:  # YOLO COCO: 2=car, 7=truck
            for (px, py, pw, ph) in parking_spots:
                # Park alanı ile araç bounding box çakışmasını kontrol et
                if px < x2 and px + pw > x1 and py < y2 and py + ph > y1:
                    color = (0, 0, 255)  # Dolu - Kırmızı
                    break
            else:
                color = (0, 255, 0)  # Boş - Yeşil

            cv2.rectangle(frame, (px, py), (px + pw, py + ph), color, 2)

    cv2.imshow('Park Alanı Durumu', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
