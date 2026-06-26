import os
import sys
import shutil
import random
import yaml

def split_data(balanced_dir, split_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Chia tập dữ liệu balanced thành các tập train/val/test theo tỷ lệ cấu hình.
    """
    print(f"Bắt đầu chia tập dữ liệu train/val/test từ {balanced_dir}...")
    print(f"Tỷ lệ chia: Train={train_ratio}, Val={val_ratio}, Test={test_ratio}")
    
    # Đảm bảo tổng tỷ lệ = 1
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-9, "Tổng tỷ lệ chia phải bằng 1.0!"
    
    if os.path.exists(split_dir):
        shutil.rmtree(split_dir)
        
    for subset in ["train", "val", "test"]:
        os.makedirs(os.path.join(split_dir, subset), exist_ok=True)
        
    # Lấy danh sách class folders và sắp xếp theo số ID của class
    def get_class_id(name):
        try:
            return int(name.split("_")[1])
        except Exception:
            return 999
            
    class_folders = sorted(
        [d for d in os.listdir(balanced_dir) if os.path.isdir(os.path.join(balanced_dir, d))],
        key=get_class_id
    )
    
    split_report = {}
    
    for folder in class_folders:
        class_path = os.path.join(balanced_dir, folder)
        images = [f for f in os.listdir(class_path) if f.endswith(".png")]
        random.shuffle(images)
        
        total_images = len(images)
        train_count = int(total_images * train_ratio)
        val_count = int(total_images * val_ratio)
        test_count = total_images - train_count - val_count # Tránh sai lệch do làm tròn
        
        # Chia ảnh
        train_imgs = images[:train_count]
        val_imgs = images[train_count:train_count + val_count]
        test_imgs = images[train_count + val_count:]
        
        # Tạo thư mục con tương ứng trong train/val/test
        for subset, subset_imgs in zip(["train", "val", "test"], [train_imgs, val_imgs, test_imgs]):
            subset_class_path = os.path.join(split_dir, subset, folder)
            os.makedirs(subset_class_path, exist_ok=True)
            for img in subset_imgs:
                shutil.copy(
                    os.path.join(class_path, img),
                    os.path.join(subset_class_path, img)
                )
                
        split_report[folder] = {
            "train": len(train_imgs),
            "val": len(val_imgs),
            "test": len(test_imgs),
            "total": total_images
        }
        print(f"  - {folder}: Train={len(train_imgs)}, Val={len(val_imgs)}, Test={len(test_imgs)} (Tổng: {total_images})")
        
    print("Chia tập dữ liệu hoàn tất!")
    return split_report, class_folders

def get_raw_counts(raw_dir):
    """
    Tính tổng số ảnh trong thư mục raw ban đầu theo từng lớp.
    Do raw_dir chia theo nguồn (gtsrb, btsc, real_world), cần gom nhóm theo class ID.
    """
    raw_counts = {}
    if not os.path.exists(raw_dir):
        return raw_counts
        
    def parse_class_id(name):
        import re
        match = re.search(r'\d+', name)
        return int(match.group(0)) if match else 999
        
    for dataset in os.listdir(raw_dir):
        dataset_path = os.path.join(raw_dir, dataset)
        if os.path.isdir(dataset_path):
            for class_folder in os.listdir(dataset_path):
                class_path = os.path.join(dataset_path, class_folder)
                if os.path.isdir(class_path):
                    class_id = parse_class_id(class_folder)
                    class_key = f"class_{class_id}"
                    
                    # Đếm số lượng ảnh trong thư mục này
                    images = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
                    raw_counts[class_key] = raw_counts.get(class_key, 0) + len(images)
                    
    return raw_counts

def get_cleaned_counts(cleaned_dir):
    """
    Tính tổng số ảnh trong thư mục cleaned theo từng lớp.
    """
    cleaned_counts = {}
    if not os.path.exists(cleaned_dir):
        return cleaned_counts
        
    for class_folder in os.listdir(cleaned_dir):
        class_path = os.path.join(cleaned_dir, class_folder)
        if os.path.isdir(class_path):
            images = [f for f in os.listdir(class_path) if os.path.isfile(os.path.join(class_path, f))]
            cleaned_counts[class_folder] = len(images)
            
    return cleaned_counts

def generate_metadata_and_report(base_dir, raw_dir, cleaned_dir, balanced_dir, split_report, class_folders):
    """
    Tạo classes.txt, data.yaml và xuất báo cáo thống kê dữ liệu dạng markdown.
    """
    # 1. Tạo classes.txt
    classes_path = os.path.join(base_dir, "classes.txt")
    with open(classes_path, "w", encoding="utf-8") as f:
        for folder in class_folders:
            f.write(f"{folder}\n")
    print(f"Đã lưu classes.txt tại: {classes_path}")
    
    # 2. Tạo data.yaml cho YOLO
    data_yaml = {
        "train": "./data/split/train",
        "val": "./data/split/val",
        "test": "./data/split/test",
        "nc": len(class_folders),
        "names": {i: folder for i, folder in enumerate(class_folders)}
    }
    
    yaml_path = os.path.join(base_dir, "data.yaml")
    with open(yaml_path, "w", encoding="utf-8") as f:
        yaml.dump(data_yaml, f, default_flow_style=False, sort_keys=False)
    print(f"Đã lưu data.yaml tại: {yaml_path}")
    
    # 3. Tổng hợp số liệu và tạo báo cáo
    raw_counts = get_raw_counts(raw_dir)
    cleaned_counts = get_cleaned_counts(cleaned_dir)
    
    report_path = os.path.join(base_dir, "data_statistics_report.md")
    
    report_content = f"""# Báo cáo Thống kê Dữ liệu Biển báo Giao thông
Báo cáo chi tiết số lượng ảnh qua các giai đoạn xử lý trong pipeline (làm sạch -> tăng cường/cân bằng -> chia tập dữ liệu).

## 1. Tóm tắt Dữ liệu
- **Tổng số lớp học (Classes):** {len(class_folders)}
- **Tỷ lệ chia dữ liệu (Train/Val/Test):** 70% / 15% / 15%
- **Đường dẫn dữ liệu kiểm thử (YOLO format):** Được cấu hình trong [data.yaml](file:///{yaml_path.replace('\\', '/')})

## 2. Bảng Phân bố Dữ liệu Qua Các Giai Đoạn

| Tên Lớp | Dữ liệu gốc (Raw) | Sau làm sạch (Cleaned) | Cân bằng & Tăng cường (Balanced) | Huấn luyện (Train) | Phát triển (Val) | Kiểm thử (Test) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
"""
    
    total_raw = 0
    total_cleaned = 0
    total_balanced = 0
    total_train = 0
    total_val = 0
    total_test = 0
    
    for folder in class_folders:
        r_cnt = raw_counts.get(folder, 0)
        c_cnt = cleaned_counts.get(folder, 0)
        b_cnt = split_report[folder]["total"]
        tr_cnt = split_report[folder]["train"]
        v_cnt = split_report[folder]["val"]
        te_cnt = split_report[folder]["test"]
        
        total_raw += r_cnt
        total_cleaned += c_cnt
        total_balanced += b_cnt
        total_train += tr_cnt
        total_val += v_cnt
        total_test += te_cnt
        
        report_content += f"| {folder} | {r_cnt} | {c_cnt} | {b_cnt} | {tr_cnt} | {v_cnt} | {te_cnt} |\n"
        
    report_content += f"| **TỔNG CỘNG** | **{total_raw}** | **{total_cleaned}** | **{total_balanced}** | **{total_train}** | **{total_val}** | **{total_test}** |\n\n"
    
    # Vẽ biểu đồ phân bố dạng ký tự (Text histogram)
    report_content += "## 3. Biểu đồ Phân bố Dữ liệu Cuối cùng (Train Set)\n"
    report_content += "```text\n"
    max_train_count = max(split_report[folder]["train"] for folder in class_folders) if class_folders else 1
    
    for folder in class_folders:
        tr_cnt = split_report[folder]["train"]
        bar_length = int((tr_cnt / max_train_count) * 40)
        bar = "█" * bar_length + "░" * (40 - bar_length)
        report_content += f"{folder:<10} | {bar} | {tr_cnt} ảnh\n"
        
    report_content += "```\n\n"
    
    report_content += """## 4. Giải thích Tiến trình Pipeline
1. **Làm sạch (Cleaning):** Loại bỏ các file hỏng, phát hiện và xóa ảnh mờ (ngưỡng Laplacian < 100), loại bỏ các ảnh trùng lặp gần tuyệt đối sử dụng thuật toán băm nhận thức 64-bit dhash.
2. **Cân bằng & Tăng cường (Augmentation):** Để tránh mất cân bằng lớp (Class Imbalance) có hại cho việc huấn luyện, hệ thống đã tăng cường ảnh cho các lớp thiểu số bằng các phép quay ngẫu nhiên, thay đổi độ sáng, độ tương phản và thêm nhiễu Gauss.
3. **Phân chia dữ liệu (Splitting):** Dữ liệu được chia ngẫu nhiên thành 3 tập riêng biệt để đảm bảo tính đánh giá khách quan của mô hình.
"""
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Đã lưu báo cáo thống kê dữ liệu tại: {report_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    balanced_dir = os.path.join(base_dir, "data", "balanced")
    split_dir = os.path.join(base_dir, "data", "split")
    
    if not os.path.exists(balanced_dir):
        print(f"Lỗi: Thư mục balanced {balanced_dir} không tồn tại!")
        print("Vui lòng chạy augmentation.py trước.")
        sys.exit(1)
        
    split_report, class_folders = split_data(balanced_dir, split_dir)
    generate_metadata_and_report(base_dir, raw_dir, cleaned_dir, balanced_dir, split_report, class_folders)
