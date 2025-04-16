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
        print(f"Không thể xử lý ảnh: {image_path}")
        return []

    # Chuẩn bị ảnh cho DNN
    h, w = processed_img.shape[:2]
    blob = cv2.dnn.blobFromImage(processed_img, 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    print(f"[INFO] Phát hiện {detections.shape[2]} đối tượng trong ảnh.")

    face_images = []
    confidence_threshold = 0.3  # Hạ ngưỡng để phát hiện nhiều hơn

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > confidence_threshold:
            # Lấy tọa độ khuôn mặt trên ảnh đã xử lý
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x, y, x2, y2) = box.astype("int")

            # Giới hạn tọa độ không vượt ngoài khung ảnh xử lý
            x = max(0, x)
            y = max(0, y)
            x2 = min(w - 1, x2)
            y2 = min(h - 1, y2)

            # Chuyển tọa độ về ảnh gốc
            scale_x = original_img.shape[1] / w
            scale_y = original_img.shape[0] / h
            x_orig = int(x * scale_x)
            y_orig = int(y * scale_y)
            x2_orig = int(x2 * scale_x)
            y2_orig = int(y2 * scale_y)

            x_orig = max(0, x_orig)
            y_orig = max(0, y_orig)
            x2_orig = min(original_img.shape[1] - 1, x2_orig)
            y2_orig = min(original_img.shape[0] - 1, y2_orig)

            # Cắt khuôn mặt từ ảnh gốc
            face = original_img[y_orig:y2_orig, x_orig:x2_orig]
            if face.size == 0:
                continue

            # Lưu ảnh khuôn mặt
            pil_image = Image.fromarray(cv2.cvtColor(face, cv2.COLOR_BGR2RGB))
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}_face{i+1}.jpg")
            pil_image.save(output_path)
            face_images.append(output_path)

            print(f"[INFO] Đã lưu khuôn mặt {i+1}: {output_path}")

    if not face_images:
        print("[INFO] Không phát hiện khuôn mặt nào vượt ngưỡng confidence.")
    return face_images
