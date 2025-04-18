from PIL import Image, ImageTk
import cv2
import numpy as np

def load_image(path, size=(120, 120)):
    try:
        img = Image.open(path)
        img.thumbnail(size)  # Chỉ thu nhỏ để hiển thị, không phóng to
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Lỗi khi tải ảnh {path}: {e}")
        return None

def preprocess_image_for_detection(image_path):
    """Tiền xử lý ảnh để cải thiện phát hiện khuôn mặt, hỗ trợ nhiều định dạng ảnh,
    tự động phóng to nếu ảnh quá nhỏ và thu nhỏ nếu quá lớn (giới hạn tối đa 300x300)."""
    try:
        # Dùng PIL để mở ảnh (hỗ trợ nhiều định dạng hơn OpenCV)
        pil_image = Image.open(image_path).convert("RGB")
        img = np.array(pil_image)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # Chuyển từ RGB sang BGR để dùng với OpenCV
    except Exception as e:
        print(f"Lỗi khi đọc ảnh {image_path}: {e}")
        return None

    # Phóng to ảnh nếu quá nhỏ
    height, width = img.shape[:2]
    if width < 100 or height < 100:
        scale = max(100 / width, 100 / height)
        img = cv2.resize(img, (int(width * scale), int(height * scale)), interpolation=cv2.INTER_LINEAR)

    # Thu nhỏ nếu ảnh quá lớn (tối đa 300x300)
    height, width = img.shape[:2]
    if width > 300 or height > 300:
        scale = min(300 / width, 300 / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return img
