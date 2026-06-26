import os
import re
import sys
import shutil
import hashlib
from PIL import Image
import numpy as np
import cv2

def dhash(image, hash_size=8):
    """
    Tính toán Difference Hash (dhash) cho một ảnh PIL.
    Đây là thuật toán băm nhận thức giúp phát hiện ảnh trùng lặp hoặc gần trùng lặp.
    """
    # Resize về kích thước (hash_size + 1, hash_size) và chuyển thành ảnh xám
    img_gray = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.array(img_gray)
    
    # Tính sự khác biệt giữa các pixel cạnh nhau trong từng hàng
    diff = pixels[:, 1:] > pixels[:, :-1]
    
    # Chuyển đổi mảng boolean thành chuỗi thập lục phân
    hash_str = ""
    for row in diff:
        val = 0
        for col in row:
            val = (val << 1) | int(col)
        hash_str += f"{val:02x}"
    return hash_str

def parse_class_id(folder_name):
    """
    Trích xuất class ID từ tên thư mục. Hỗ trợ các định dạng:
    - class_0 -> 0
    - 00005 -> 5
    - 3 -> 3
    """
    match = re.search(r'\d+', folder_name)
    if match:
        return int(match.group(0))
    # Nếu không có số, băm tên thư mục để có một ID duy nhất
    return int(hashlib.md5(folder_name.encode()).hexdigest(), 16) % 1000

def clean_dataset(raw_dir, cleaned_dir, target_size=(64, 64), blur_threshold=100.0):
    """
    Duyệt qua dữ liệu gốc, làm sạch và lưu sang thư mục cleaned_dir.
    """
    print(f"Khởi động tiến trình làm sạch dữ liệu từ {raw_dir}...")
    print(f"Kích thước chuẩn hóa: {target_size}, Ngưỡng lọc mờ (Laplacian var): {blur_threshold}")
    
    if os.path.exists(cleaned_dir):
        shutil.rmtree(cleaned_dir)
    os.makedirs(cleaned_dir, exist_ok=True)
    
    # Thống kê
    stats = {
        "total_processed": 0,
        "corrupt_removed": 0,
        "blurry_removed": 0,
        "duplicate_removed": 0,
        "saved": 0
    }
    
    # Tập hợp các mã hash đã thấy để lọc ảnh trùng lặp trên toàn bộ tập dữ liệu
    seen_hashes = set()
    
    # Duyệt qua các dataset (gtsrb, btsc, real_world)
    for dataset in os.listdir(raw_dir):
        dataset_path = os.path.join(raw_dir, dataset)
        if not os.path.isdir(dataset_path):
            continue
            
        print(f"Đang xử lý dataset: {dataset}")
        
        # Duyệt qua các thư mục lớp
        for class_folder in os.listdir(dataset_path):
            class_path = os.path.join(dataset_path, class_folder)
            if not os.path.isdir(class_path):
                continue
                
            class_id = parse_class_id(class_folder)
            target_class_folder = f"class_{class_id}"
            target_class_path = os.path.join(cleaned_dir, target_class_folder)
            os.makedirs(target_class_path, exist_ok=True)
            
            # Duyệt qua từng ảnh trong lớp
            for img_name in os.listdir(class_path):
                img_path = os.path.join(class_path, img_name)
                if not os.path.isfile(img_path):
                    continue
                
                stats["total_processed"] += 1
                
                # 1. Kiểm tra ảnh lỗi (Corrupted)
                try:
                    with Image.open(img_path) as img:
                        img.verify() # Kiểm tra tính toàn vẹn file sơ bộ
                    
                    # verify() đóng file, cần mở lại để đọc dữ liệu
                    img = Image.open(img_path)
                    img.load()
                except Exception:
                    stats["corrupt_removed"] += 1
                    continue
                
                # 2. Chuẩn hóa kích thước
                # Chuyển hệ màu RGB nếu ảnh đang ở hệ màu khác (như RGBA, Grayscale, P)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                img_resized = img.resize(target_size, Image.Resampling.LANCZOS)
                
                # 3. Phát hiện ảnh mờ (Blur detection bằng Laplacian Variance)
                img_np = np.array(img_resized)
                img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
                lap_var = cv2.Laplacian(img_gray, cv2.CV_64F).var()
                
                if lap_var < blur_threshold:
                    stats["blurry_removed"] += 1
                    continue
                
                # 4. Phát hiện ảnh trùng lặp (Duplicate detection bằng dhash)
                img_hash = dhash(img_resized)
                if img_hash in seen_hashes:
                    stats["duplicate_removed"] += 1
                    continue
                seen_hashes.add(img_hash)
                
                # 5. Lưu ảnh sạch
                new_img_name = f"{dataset}_{class_folder}_{img_name}"
                # Đổi đuôi mở rộng sang png để thống nhất định dạng ảnh sạch
                new_img_name = os.path.splitext(new_img_name)[0] + ".png"
                img_resized.save(os.path.join(target_class_path, new_img_name), "PNG")
                stats["saved"] += 1
                
    # In báo cáo kết quả làm sạch
    print("\n--- KẾT QUẢ LÀM SẠCH DỮ LIỆU ---")
    print(f"Tổng số ảnh quét qua: {stats['total_processed']}")
    print(f"Ảnh hỏng bị loại bỏ: {stats['corrupt_removed']}")
    print(f"Ảnh mờ bị loại bỏ:  {stats['blurry_removed']}")
    print(f"Ảnh trùng bị loại bỏ: {stats['duplicate_removed']}")
    print(f"Ảnh sạch được lưu:   {stats['saved']}")
    print("---------------------------------")
    return stats

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    
    if not os.path.exists(raw_dir):
        print(f"Lỗi: Thư mục dữ liệu gốc {raw_dir} không tồn tại!")
        print("Vui lòng chạy mock_data_generator.py trước.")
        sys.exit(1)
        
    clean_dataset(raw_dir, cleaned_dir)
