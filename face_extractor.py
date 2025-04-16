import cv2
import os
from PIL import Image
from utils import preprocess_image_for_detection

def extract_faces(image_path, output_dir):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Đọc ảnh gốc để lưu kết quả
    original_img = cv2.imread(image_path)
    if original_img is None:
        print(f"Không thể đọc ảnh: {image_path}")
        return []

    # Tiền xử lý ảnh để phát hiện khuôn mặt
    processed_img = preprocess_image_for_detection(image_path)
    if processed_img is None:
        print(f"Không thể đọc ảnh: {image_path}")
        return []

    gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

    face_images = []
    for i, (x, y, w, h) in enumerate(faces):
        # Tính toán lại tọa độ trên ảnh gốc
        height_processed, width_processed = processed_img.shape[:2]
        height_orig, width_orig = original_img.shape[:2]
        scale_x = width_orig / width_processed
        scale_y = height_orig / height_processed
        x_orig, y_orig = int(x * scale_x), int(y * scale_y)
        w_orig, h_orig = int(w * scale_x), int(h * scale_y)

        # Cắt khuôn mặt từ ảnh gốc
        face = original_img[y_orig:y_orig+h_orig, x_orig:x_orig+w_orig]
        pil_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
        output_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_face{i+1}.jpg")
        pil_image.save(output_path)
        face_images.append(output_path)

    return face_images