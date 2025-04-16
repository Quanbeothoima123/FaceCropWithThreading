# import cv2
# import os
# from PIL import Image
# from utils import preprocess_image_for_detection

# def extract_faces(image_path, output_dir):
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#     # Đọc ảnh gốc để lưu kết quả
#     original_img = cv2.imread(image_path)
#     if original_img is None:
#         print(f"Không thể đọc ảnh: {image_path}")
#         return []

#     # Tiền xử lý ảnh để phát hiện khuôn mặt
#     processed_img = preprocess_image_for_detection(image_path)
#     if processed_img is None:
#         print(f"Không thể đọc ảnh: {image_path}")
#         return []

#     gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3)

#     face_images = []
#     for i, (x, y, w, h) in enumerate(faces):
#         # Tính toán lại tọa độ trên ảnh gốc
#         height_processed, width_processed = processed_img.shape[:2]
#         height_orig, width_orig = original_img.shape[:2]
#         scale_x = width_orig / width_processed
#         scale_y = height_orig / height_processed
#         x_orig, y_orig = int(x * scale_x), int(y * scale_y)
#         w_orig, h_orig = int(w * scale_x), int(h * scale_y)

#         # Cắt khuôn mặt từ ảnh gốc
#         face = original_img[y_orig:y_orig+h_orig, x_orig:x_orig+w_orig]
#         pil_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
#         output_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_face{i+1}.jpg")
#         pil_image.save(output_path)
#         face_images.append(output_path)

#     return face_images



import cv2
import os
import numpy as np
from PIL import Image
from utils import preprocess_image_for_detection

def extract_faces(image_path, output_dir):
    # Tải mô hình DNN face detector
    model_file = "models/res10_300x300_ssd_iter_140000.caffemodel"
    config_file = "models/deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(config_file, model_file)

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

    # Chuẩn bị ảnh cho DNN
    h, w = processed_img.shape[:2]
    blob = cv2.dnn.blobFromImage(processed_img, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    face_images = []
    # Ngưỡng độ tin cậy
    confidence_threshold = 0.5

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            # Lấy tọa độ khuôn mặt
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x2, y2) = box.astype("int")
            x, y, w, h = x, y, x2 - x, y2 - y

            # Tính toán lại tọa độ trên ảnh gốc
            height_processed, width_processed = processed_img.shape[:2]
            height_orig, width_orig = original_img.shape[:2]
            scale_x = width_orig / width_processed
            scale_y = height_orig / height_processed
            x_orig, y_orig = int(x * scale_x), int(y * scale_y)
            w_orig, h_orig = int(w * scale_x), int(h * scale_y)

            # Cắt khuôn mặt từ ảnh gốc
            face = original_img[y_orig:y_orig+h_orig, x_orig:x_orig+w_orig]
            if face.size == 0:  # Kiểm tra vùng cắt hợp lệ
                continue
            pil_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
            output_path = os.path.join(output_dir, f"{os.path.basename(image_path)}_face{i+1}.jpg")
            pil_image.save(output_path)
            face_images.append(output_path)

    return face_images