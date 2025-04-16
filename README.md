# Face Extractor GUI

Chương trình giúp **tách tất cả khuôn mặt** có trong một ảnh đầu vào và lưu lại từng khuôn mặt thành file ảnh riêng. Giao diện đơn giản, dễ sử dụng, và sử dụng mô hình DNN của OpenCV để phát hiện khuôn mặt.

---

##  Tính năng chính

- Hỗ trợ **ảnh nhiều định dạng**: `.jpg`, `.jpeg`, `.png`, `.bmp`, v.v.
- **Phát hiện nhiều khuôn mặt** trong cùng một ảnh.
- **Lưu từng khuôn mặt** thành ảnh riêng trong thư mục chỉ định.
- Giới hạn xử lý ảnh có kích thước tối đa **300x300** (ảnh lớn hơn sẽ được thu nhỏ lại).

---

##  Mô hình sử dụng

- `res10_300x300_ssd_iter_140000.caffemodel`
- `deploy.prototxt`

Đây là mô hình DNN SSD pretrained của OpenCV để phát hiện khuôn mặt.


## Cài đặt

### 1. Tạo môi trường và cài thư viện

pip install -r requirements.txt

##  Cách sử dụng
Terminal bấm : 
python main.py 
rồi enter

### 2. Hướng dẫn sử dụng giao diện
Nhấn Chọn ảnh → chọn một ảnh từ máy tính.

Ảnh sẽ hiển thị ở khung bên trái.

Nhấn Tách khuôn mặt → chương trình sẽ:

Thu nhỏ ảnh nếu lớn hơn 300x300.

Tách tất cả khuôn mặt có confidence =0.3.

Lưu kết quả vào thư mục output/.

### Lưu ý
Nếu không phát hiện được khuôn mặt, giảm confidence_threshold  trong mã nguồn nhưng các khuôn mặt sẽ có những hình ảnh không phải mặt người cũng được tách

### Link youtobe chạy thử
https://youtu.be/1rb_yACxACc


### NGười thực hiện 
# Cấn Anh Quân -22810310260
