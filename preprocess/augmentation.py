import os
import sys
import shutil
import random
from PIL import Image, ImageEnhance
import numpy as np

def apply_random_augmentation(image):
    """
    Áp dụng ngẫu nhiên các phép tăng cường dữ liệu lên ảnh PIL.
    """
    # 1. Quay ngẫu nhiên từ -15 đến 15 độ
    if random.random() > 0.5:
        angle = random.uniform(-15, 15)
        # Sử dụng màu xám trung tính (128,128,128) để làm đầy phần thừa khi quay
        image = image.rotate(angle, resample=Image.Resampling.BILINEAR, expand=False, fillcolor=(128, 128, 128))
    
    # 2. Dịch chuyển ngẫu nhiên (Translation) tối đa 10% kích thước
    if random.random() > 0.5:
        width, height = image.size
        tx = random.uniform(-0.1, 0.1) * width
        ty = random.uniform(-0.1, 0.1) * height
        # Ma trận biến đổi affine: [1, 0, tx, 0, 1, ty]
        image = image.transform(image.size, Image.Transform.AFFINE, (1, 0, tx, 0, 1, ty), 
                                resample=Image.Resampling.BILINEAR, fillcolor=(128, 128, 128))
        
    # 3. Thay đổi độ sáng ngẫu nhiên (0.7 đến 1.3)
    if random.random() > 0.5:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))
        
    # 4. Thay đổi độ tương phản ngẫu nhiên (0.7 đến 1.3)
    if random.random() > 0.5:
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(random.uniform(0.7, 1.3))
        
    # 5. Thêm nhiễu Gauss ngẫu nhiên
    if random.random() > 0.5:
        img_np = np.array(image).astype(np.float32)
        noise = np.random.normal(0, random.uniform(5.0, 15.0), img_np.shape)
        img_np = np.clip(img_np + noise, 0, 255).astype(np.uint8)
        image = Image.fromarray(img_np)
        
    return image

def balance_dataset(cleaned_dir, balanced_dir, target_count=None, strict_balance=True):
    """
    Cân bằng số lượng ảnh giữa các lớp và thực hiện Data Augmentation.
    """
    print(f"Bắt đầu cân bằng và tăng cường dữ liệu từ {cleaned_dir}...")
    
    if os.path.exists(balanced_dir):
        shutil.rmtree(balanced_dir)
    os.makedirs(balanced_dir, exist_ok=True)
    
    # Đếm số lượng ảnh ban đầu của từng lớp
    class_images = {}
    for class_folder in os.listdir(cleaned_dir):
        class_path = os.path.join(cleaned_dir, class_folder)
        if os.path.isdir(class_path):
            images = [f for f in os.listdir(class_path) if f.endswith(".png")]
            class_images[class_folder] = images
            
    if not class_images:
        print("Lỗi: Không tìm thấy lớp dữ liệu nào trong thư mục cleaned!")
        return
        
    # Xác định số lượng ảnh mục tiêu
    max_count = max(len(imgs) for imgs in class_images.values())
    if target_count is None:
        # Mặc định lấy số lượng ảnh của lớp lớn nhất hoặc tối thiểu 100 ảnh để mô hình đủ dữ liệu học
        target_count = max(100, max_count)
        
    print(f"Số lượng ảnh mục tiêu cho mỗi lớp: {target_count} (strict_balance={strict_balance})")
    
    # Lưu thống kê số lượng
    balance_report = {}
    
    for class_folder, images in class_images.items():
        original_count = len(images)
        class_balanced_path = os.path.join(balanced_dir, class_folder)
        os.makedirs(class_balanced_path, exist_ok=True)
        
        print(f"Xử lý {class_folder}: Có {original_count} ảnh")
        
        if original_count == 0:
            print(f"  Bỏ qua {class_folder} vì không có ảnh nào.")
            continue
            
        # Copy các ảnh gốc sang thư mục cân bằng trước
        copied_count = 0
        if strict_balance and original_count > target_count:
            # Downsampling: Chỉ chọn ngẫu nhiên target_count ảnh gốc
            selected_images = random.sample(images, target_count)
            for img_name in selected_images:
                shutil.copy(
                    os.path.join(cleaned_dir, class_folder, img_name),
                    os.path.join(class_balanced_path, img_name)
                )
            copied_count = target_count
            augmented_count = 0
        else:
            # Giữ lại toàn bộ ảnh gốc
            for img_name in images:
                shutil.copy(
                    os.path.join(cleaned_dir, class_folder, img_name),
                    os.path.join(class_balanced_path, img_name)
                )
            copied_count = original_count
            
            # Cần tạo thêm bao nhiêu ảnh augmentation
            needed = target_count - original_count
            augmented_count = 0
            
            if needed > 0:
                # Thực hiện Augmentation tuần hoàn trên các ảnh gốc có sẵn
                for i in range(needed):
                    base_img_name = images[i % original_count]
                    base_img_path = os.path.join(cleaned_dir, class_folder, base_img_name)
                    
                    try:
                        with Image.open(base_img_path) as img:
                            aug_img = apply_random_augmentation(img)
                            aug_name = f"aug_{i:04d}_{base_img_name}"
                            aug_img.save(os.path.join(class_balanced_path, aug_name), "PNG")
                            augmented_count += 1
                    except Exception as e:
                        print(f"  Lỗi khi tăng cường ảnh {base_img_name}: {e}")
                        
        final_count = copied_count + augmented_count
        balance_report[class_folder] = {
            "original": original_count,
            "augmented": augmented_count,
            "final": final_count
        }
        print(f"  -> Kết quả: {final_count} ảnh (Gốc: {copied_count}, Tăng cường: {augmented_count})")
        
    print("Cân bằng dữ liệu hoàn tất!")
    return balance_report

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    balanced_dir = os.path.join(base_dir, "data", "balanced")
    
    if not os.path.exists(cleaned_dir):
        print(f"Lỗi: Thư mục cleaned {cleaned_dir} không tồn tại!")
        print("Vui lòng chạy data_cleaning.py trước.")
        sys.exit(1)
        
    balance_dataset(cleaned_dir, balanced_dir)
