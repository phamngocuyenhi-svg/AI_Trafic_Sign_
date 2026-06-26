import os
import random
import shutil
from PIL import Image, ImageDraw, ImageFilter

def generate_mock_traffic_sign(class_id, size=(100, 100), blur=False, corrupt=False):
    """
    Tạo một ảnh biển báo giao thông giả lập bằng PIL.
    """
    if corrupt:
        return b"broken image file content"
    
    # Tạo ảnh nền xám/trắng ngẫu nhiên
    bg_color = (random.randint(200, 240), random.randint(200, 240), random.randint(200, 240))
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Vẽ hình dạng biển báo dựa trên class_id
    shape_type = class_id % 4
    if shape_type == 0:
        # Biển tròn viền đỏ (Cấm / Tốc độ)
        draw.ellipse([10, 10, size[0]-10, size[1]-10], fill=(220, 20, 60), outline=(255, 255, 255), width=4)
        draw.ellipse([20, 20, size[0]-20, size[1]-20], fill=(255, 255, 255))
    elif shape_type == 1:
        # Biển vuông xanh lam (Chỉ dẫn)
        draw.rectangle([10, 10, size[0]-10, size[1]-10], fill=(30, 144, 255), outline=(255, 255, 255), width=4)
    elif shape_type == 2:
        # Biển tam giác viền đỏ nền vàng (Nguy hiểm)
        draw.polygon([(size[0]//2, 10), (10, size[1]-10), (size[0]-10, size[1]-10)], fill=(255, 215, 0), outline=(220, 20, 60), width=4)
    else:
        # Biển tròn xanh lam (Hiệu lệnh)
        draw.ellipse([10, 10, size[0]-10, size[1]-10], fill=(0, 0, 205), outline=(255, 255, 255), width=4)
        
    # Vẽ chữ số/biểu tượng đặc trưng cho từng lớp để tạo sự khác biệt về nội dung ảnh (giúp phân biệt dhash)
    color_r = (class_id * 45) % 256
    color_g = (100 + class_id * 35) % 256
    color_b = (200 - class_id * 25) % 256
    
    # Vẽ các hình học nhỏ khác nhau dựa trên class_id
    inner_shape = class_id % 3
    if inner_shape == 0:
        draw.ellipse([size[0]//2 - 15, size[1]//2 - 15, size[0]//2 + 15, size[1]//2 + 15], fill=(color_r, color_g, color_b))
    elif inner_shape == 1:
        draw.rectangle([size[0]//2 - 12, size[1]//2 - 12, size[0]//2 + 12, size[1]//2 + 12], fill=(color_r, color_g, color_b))
    else:
        draw.polygon([(size[0]//2, size[1]//2 - 15), (size[0]//2 - 15, size[1]//2 + 15), (size[0]//2 + 15, size[1]//2 + 15)], fill=(color_r, color_g, color_b))
    
    if blur:
        img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(4.0, 6.0)))
        
    return img

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    
    # Reset raw data if exists
    if os.path.exists(raw_dir):
        shutil.rmtree(raw_dir)
        
    datasets = ["gtsrb", "btsc", "real_world"]
    # Số lớp cho từng dataset
    classes = {
        "gtsrb": [0, 1, 2, 3, 4],     # 5 lớp biển báo
        "btsc": [0, 1, 3, 5],         # 4 lớp biển báo (trùng một số lớp với GTSRB)
        "real_world": [2, 4, 6]       # 3 lớp biển báo
    }
    
    # Số lượng ảnh phân bố không đều để tạo mất cân bằng lớp
    # Lớp 0: Nhiều (150 ảnh)
    # Lớp 1: Vừa (80 ảnh)
    # Lớp 2: Ít (15 ảnh) - Cần được cân bằng bằng Augmentation
    # Lớp 3: Trung bình (45 ảnh)
    # Lớp 4: Cực ít (5 ảnh)
    # Lớp 5: Rất ít (8 ảnh)
    # Lớp 6: Trung bình (35 ảnh)
    
    class_counts = {
        0: 150,
        1: 80,
        2: 15,
        3: 45,
        4: 5,
        5: 8,
        6: 35
    }
    
    print("Bắt đầu sinh dữ liệu biển báo giả lập...")
    
    for dataset in datasets:
        dataset_path = os.path.join(raw_dir, dataset)
        os.makedirs(dataset_path, exist_ok=True)
        
        for c in classes[dataset]:
            class_name = f"class_{c}"
            class_path = os.path.join(dataset_path, class_name)
            os.makedirs(class_path, exist_ok=True)
            
            # Tính số ảnh cần sinh cho dataset này của lớp c
            # Chia đều số ảnh theo class_counts
            count = class_counts[c] // 2 if dataset != "real_world" else class_counts[c] // 4
            count = max(1, count)
            
            # Tạo ảnh trùng lặp để lọc
            duplicate_img = None
            
            for i in range(count):
                img_name = f"sign_{i:04d}.png"
                img_path = os.path.join(class_path, img_name)
                
                # Quyết định xem ảnh có lỗi/mờ/trùng lặp không
                is_corrupt = (i == 0 and c == 0) # Ảnh đầu tiên của lớp 0 bị hỏng
                is_blurry = (i == 2 and c == 1) or (i == 1 and c == 2) # Một số ảnh bị mờ
                is_duplicate = (i >= 5 and i < 8 and c == 0) # Lớp 0 có ảnh trùng lặp
                
                if is_corrupt:
                    with open(img_path, "wb") as f:
                        f.write(generate_mock_traffic_sign(c, corrupt=True))
                    # Tạo thêm ảnh có kích thước sai
                    wrong_img = Image.new("RGB", (10, 10), color=(0, 0, 0))
                    wrong_img.save(os.path.join(class_path, f"sign_wrong_size_{i}.png"))
                elif is_duplicate:
                    if duplicate_img is None:
                        duplicate_img = generate_mock_traffic_sign(c)
                    duplicate_img.save(img_path)
                else:
                    img = generate_mock_traffic_sign(c, blur=is_blurry)
                    img.save(img_path)
                    
            print(f"  - Đã sinh dữ liệu cho: {dataset} / {class_name} ({count} ảnh)")
            
    print("Sinh dữ liệu giả lập hoàn tất!")
    print(f"Dữ liệu gốc được lưu tại: {raw_dir}")

if __name__ == "__main__":
    main()
