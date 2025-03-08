import cv2
import matplotlib.pyplot as plt
import numpy as np

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

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Adaptive thresholding kullanımı
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    for (x, y, w, h) in parking_spots:
        roi = thresh[y:y+h, x:x+w]
        white_pixels = cv2.countNonZero(roi)

        # Beyaz piksellerin oranını kontrol et
        if white_pixels > (w * h) * 0.5:
            color = (0, 0, 255)  # Dolu - Kırmızı
        else:
            color = (0, 255, 0)  # Boş - Yeşil

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    cv2.imshow('Park Alanı Durumu', frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
