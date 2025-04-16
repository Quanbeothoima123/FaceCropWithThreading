import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, Canvas, Frame
from face_extractor import extract_faces
from utils import load_image

class FaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chương trình tách khuôn mặt ra khỏi ảnh")
        self.image_paths = []
        self.face_paths = []
        self.current_image_index = 0

        self.build_gui()

    def build_gui(self):
        # Nút chọn thư mục
        self.select_btn = tk.Button(self.root, text="Chọn thư mục có hình ảnh", bg="salmon", command=self.select_images)
        self.select_btn.pack(pady=5)

        # Vùng hiển thị ảnh gốc
        self.left_frame = self.create_scroll_area("Các hình ảnh ở thư mục gốc", "pink")
        self.left_frame.pack(side="left", padx=10)

        # Nút xử lý
        self.process_btn = tk.Button(self.root, text="Bấm để tách khuôn mặt", bg="khaki", command=self.start_thread)
        self.process_btn.pack(pady=5)

        # Vùng hiển thị ảnh khuôn mặt
        self.right_frame = self.create_scroll_area("Hình ảnh khuôn mặt được tách", "cyan")
        self.right_frame.pack(side="right", padx=10)

        # Trạng thái xử lý
        self.progress_var = tk.StringVar(value="Chọn ảnh để bắt đầu xử lý!")
        self.progress_label = tk.Label(self.root, textvariable=self.progress_var, bg="white")
        self.progress_label.pack(pady=5)

        # Thanh tiến trình
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack(pady=5)

    def create_scroll_area(self, label_text, bg):
        frame = Frame(self.root)
        label = tk.Label(frame, text=label_text)
        label.pack()

        canvas = Canvas(frame, width=240, height=300, bg=bg)
        scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = Frame(canvas, bg=bg)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        frame.scroll_frame = scroll_frame
        return frame

    def select_images(self):
        paths = filedialog.askopenfilenames(title="Chọn ảnh", filetypes=[("Image files", "*.jpg *.png")])
        if paths:
            self.image_paths = list(set(paths))  # Loại bỏ trùng lặp
            self.display_images(self.left_frame.scroll_frame, self.image_paths)
            self.progress_var.set("Nhấn 'Bấm để tách khuôn mặt' để xử lý!")

    def display_images(self, container, paths):
        for widget in container.winfo_children():
            widget.destroy()
        for path in paths:
            img = load_image(path)
            if img:
                label = tk.Label(container, image=img)
                label.image = img
                label.pack(pady=2)

    def start_thread(self):
        if not self.image_paths:
            messagebox.showwarning("Chưa chọn ảnh", "Vui lòng chọn ảnh trước khi xử lý.")
            return
        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = len(self.image_paths)
        self.current_image_index = 0
        self.progress_var.set(f"Đang xử lý: {os.path.basename(self.image_paths[0])}")
        thread = threading.Thread(target=self.process_images)
        thread.start()
        self.update_progress()

    def update_progress(self):
        if self.current_image_index < len(self.image_paths):
            # Cập nhật trạng thái sau khi xử lý xong một ảnh
            if self.current_image_index > 0:
                self.progress_var.set(f"Xử lý xong: {os.path.basename(self.image_paths[self.current_image_index - 1])}")
            self.progress_bar["value"] = self.current_image_index
            self.root.after(100, self.update_progress)
        else:
            self.progress_var.set("Chọn ảnh khác để xử lý nào!")
            self.progress_bar["value"] = len(self.image_paths)

    def process_images(self):
        self.face_paths.clear()
        output_dir = "faces"
        os.makedirs(output_dir, exist_ok=True)

        for i, img_path in enumerate(self.image_paths):
            self.current_image_index = i
            faces = extract_faces(img_path, output_dir)
            self.face_paths.extend(faces)
            # Cập nhật trạng thái sau khi xử lý xong một ảnh
            self.root.after_idle(lambda: self.progress_var.set(
                f"Xử lý xong: {os.path.basename(img_path)}" if i < len(self.image_paths) - 1 else 
                f"Đang xử lý: {os.path.basename(self.image_paths[i + 1])}" if i + 1 < len(self.image_paths) else 
                "Chọn ảnh khác để xử lý nào!"
            ))
            self.current_image_index = i + 1

        self.root.after_idle(lambda: self.display_images(self.right_frame.scroll_frame, self.face_paths))

def run():
    root = tk.Tk()
    app = FaceApp(root)
    root.mainloop()