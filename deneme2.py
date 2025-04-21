import cv2

# Görseli yükle
img = cv2.imread(r"C:\Users\eeshn\Desktop\carpark.jpg")

# Tıklanan noktaları burada tutacağız
points = []

# Mouse click callback
def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        print(f"Koordinat: ({x}, {y})")

        # Noktayı görsele çiz
        cv2.circle(img, (x, y), 5, (0, 255, 0), cv2.FILLED)

cv2.imshow("Gorsel", img)
cv2.setMouseCallback("Gorsel", mouseClick)

while True:
    cv2.imshow("Gorsel", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()

# En son koordinatları çıktı al
print("Seçilen Koordinatlar:")
print(points)
