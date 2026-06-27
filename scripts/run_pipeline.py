import os
import time
import sys

# Thêm thư mục scripts vào python path để import chéo
scripts_dir = os.path.dirname(os.path.abspath(__file__))
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from data_cleaning import clean_dataset
from augmentation import balance_dataset
from split_dataset import split_data, generate_metadata_and_report

def main():
    start_time = time.time()
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, "data", "raw")
    cleaned_dir = os.path.join(base_dir, "data", "cleaned")
    balanced_dir = os.path.join(base_dir, "data", "balanced")
    split_dir = os.path.join(base_dir, "data", "split")
    
    print("="*60)
    print("KHỞI CHẠY PIPELINE TIỀN XỬ LÝ DỮ LIỆU BIỂN BÁO GIAO THÔNG")
    print("="*60)
    
    # Kiểm tra sự tồn tại của dữ liệu gốc
    if not os.path.exists(raw_dir) or not os.listdir(raw_dir):
        print(f"Lỗi: Thư mục dữ liệu gốc trống hoặc không tồn tại: {raw_dir}")
        print("Vui lòng chạy script download_data.py để tải dữ liệu trước.")
        sys.exit(1)
            
    # Bước 1: Làm sạch dữ liệu
    step1_start = time.time()
    print("\n--- BƯỚC 1: LÀM SẠCH VÀ CHUẨN HÓA DỮ LIỆU ---")
    clean_stats = clean_dataset(raw_dir, cleaned_dir)
    print(f"Hoàn thành Bước 1 trong {time.time() - step1_start:.2f} giây.")
    
    # Bước 2: Cân bằng lớp & Tăng cường dữ liệu
    step2_start = time.time()
    print("\n--- BƯỚC 2: CÂN BẰNG LỚP VÀ DATA AUGMENTATION ---")
    # Tự động lấy số lượng ảnh cân bằng là max(100, max_count_in_cleaned)
    balance_report = balance_dataset(cleaned_dir, balanced_dir, strict_balance=True)
    print(f"Hoàn thành Bước 2 trong {time.time() - step2_start:.2f} giây.")
    
    # Bước 3: Phân chia tập dữ liệu train/val/test và xuất báo cáo
    step3_start = time.time()
    print("\n--- BƯỚC 3: PHÂN CHIA TRAIN/VAL/TEST & XUẤT CẤU HÌNH ---")
    split_report, class_folders = split_data(balanced_dir, split_dir)
    generate_metadata_and_report(base_dir, raw_dir, cleaned_dir, balanced_dir, split_report, class_folders)
    print(f"Hoàn thành Bước 3 trong {time.time() - step3_start:.2f} giây.")
    
    total_time = time.time() - start_time
    print("="*60)
    print("PIPELINE ĐÃ CHẠY HOÀN THÀNH THÀNH CÔNG!")
    print(f"Tổng thời gian thực thi: {total_time:.2f} giây")
    print(f"Đường dẫn báo cáo chi tiết: {os.path.join(base_dir, 'data_statistics_report.md')}")
    print("="*60)

if __name__ == "__main__":
    main()
